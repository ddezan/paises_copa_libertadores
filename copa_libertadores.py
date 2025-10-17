# Desenvolvido por Daniel Dezan Lopes da Silva em 17/10/2025

import pandas as pd         # Manipulação e análise de dados.
import requests             # Fazer requisições HTTP em Python
import io                   # Permite ler e escrever dados em diferentes formatos, como texto, bytes, etc.
import re                   # Trabalhar com expressões regulares em Python
import plotly.express as px # Criar visualizações de dados / gráficos interativos


# Função para extrair o número de títulos
def extrair_numero(titulo):
    """
        Extrai o número de títulos de uma string.

        Args:
            titulo (str): A string que contém o número de títulos.

        Returns:
            int: O número de títulos encontrado na string. Se nenhum número for encontrado, retorna 0.
    """
    
    match = re.search(r'(\d+)', str(titulo))  # Converte titulo para string e encontra o número
    if match:
        return int(match.group(1))
    else:
        return 0


# Site fonte dos dados
url = 'https://pt.wikipedia.org/wiki/Copa_Libertadores_da_Am%C3%A9rica'

# Define os cabeçalhos da requisição HTTP. Os cabeçalhos são usados para fornecer informações adicionais sobre a requisição. 
# Nesse caso, o cabeçalho User-Agent é usado para identificar o navegador que está fazendo a requisição. 
# Isso é útil para evitar que o servidor bloqueie a requisição por ser de um script automatizado.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Envia uma requisição HTTP GET para a URL especificada e armazena a resposta na variável response. 
# O parâmetro headers=headers especifica os cabeçalhos da requisição.
response = requests.get(url, headers=headers)

# Lê as tabelas HTML presentes na página web e as armazena em uma lista de DataFrames do pandas. 
# A função StringIO(response.text) é usada para converter a resposta da requisição em um objeto de arquivo que pode ser lido pela função read_html.
dfs = pd.read_html(io.StringIO(response.text))

# Seleciona a 12ª tabela da lista de tabelas lidas da página web
df_temp = dfs[11]

# Seleciona apenas as colunas 'País' e 'Títulos' da tabela df_temp e as armazena em uma nova variável df_final
df_final = df_temp[['País', 'Títulos']].copy()

# Imprime versão inicial da tabela. Útil para acompanhamento das transformações, mas não necessária.
print('\nVersão inicial da tabela\n')
print(df_final)

# Aplica a função 'extrair_numero' à coluna 'Títulos'
df_final['Numero_Titulos'] = df_final['Títulos'].apply(extrair_numero)

# Remove as linhas com 0 títulos
df_final = df_final[df_final['Numero_Titulos'] > 0]

# Remove a coluna 'Numero_Titulos'
df_final = df_final[['País', 'Títulos']]

# Imprime versão da tabela com alguns tratamentos
print('\n---------------------------------------------------------------------\n')
print('Versão tratada da tabela\n')
print(df_final)

# Remove o número de títulos e extrai os anos
#
# r'^\d+\s*\((.*)\)$': Essa é a expressão regular usada para encontrar o padrão nas strings. Vamos quebrá-la:
#    - ^: Indica o início da string.
#    - \d+: Encontra um ou mais dígitos (0-9).
#    - \s*: Encontra zero ou mais espaços em branco.
#    - \( e \): Encontram os parênteses literais.
#    - (.*): É um grupo de captura que encontra qualquer caractere (exceto newline) entre os parênteses.
#    - $: Indica o final da string.
#
# r'\1': Essa é a string de substituição. O \1 refere-se ao grupo de captura na expressão regular, que são os anos entre os parênteses.
#
# regex=True: Especifica que a string de busca é uma expressão regular.
df_final['Títulos'] = df_final['Títulos'].str.replace(r'^\d+\s*\((.*)\)$', r'\1', regex=True).copy()

# Agrupa os anos por país
#
# .groupby('País'):Essa parte da linha agrupa o DataFrame resultante pelo campo 'País'.
# ['Títulos']: Essa parte da linha seleciona apenas a coluna 'Títulos' do DataFrame agrupado.
# .apply(lambda x: ', '.join(x).split(', ')): 
# A função lambda faz o seguinte:
# ', '.join(x): Junta todas as strings de anos em uma única string separada por vírgulas e espaços.
# .split(', '): Divide a string resultante em uma lista de strings, usando a vírgula e o espaço como separadores.
df_grouped = df_final.groupby('País')['Títulos'].apply(lambda x: ', '.join(x).split(', ')).reset_index()

# Remove as separações de anos com letra 'e'
# [i.split(' e ') for i in x]: Essa parte da função lambda divide cada string de anos em uma lista de strings, usando a palavra "e" como separador.
# [item for sublist in ... for item in sublist]: Essa parte da função lambda é uma forma de achatar a lista de listas em uma lista simples.
df_grouped['Títulos'] = df_grouped['Títulos'].apply(lambda x: [item for sublist in [i.split(' e ') for i in x] for item in sublist])

# Imprime o resultado da tabela já com os agrupamentos
print('\n---------------------------------------------------------------------\n')
print('Tabela Agrupada\n')
print(df_grouped)

# Explode a lista de anos em linhas separadas
df_exploded = df_grouped.explode('Títulos')

# Converter os anos para inteiros
df_exploded['Títulos'] = df_exploded['Títulos'].astype(int)

# Pivotar o dataframe para ter países como colunas
df_pivot = df_exploded.pivot_table(index='Títulos', columns='País', aggfunc='size', fill_value=0)

# Calcular o total cumulativo por país
df_cumsum = df_pivot.cumsum()

# Imprime o resultado
print('\n---------------------------------------------------------------------\n')
print('Tabela Final\n')
print(df_cumsum)

# Gerar o gráfico de linhas
fig = px.line(df_cumsum, x=df_cumsum.index, y=df_cumsum.columns, title='Títulos da Copa Libertadores por País e Ano')
fig.update_layout(xaxis_title='Ano', yaxis_title='Quantidade de Títulos')
fig.write_html('grafico_linhas.html')