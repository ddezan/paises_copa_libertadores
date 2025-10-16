import pandas as pd
import requests

url = "https://pt.wikipedia.org/wiki/Copa_Libertadores_da_Am%C3%A9rica"

# Fazer a requisição com cabeçalhos legítimos
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)

# Ler as tabelas do HTML
dfs = pd.read_html(response.text)

# Salva a tabela desejada
df_temp = dfs[11]

# Salva as colunas de interesse
df_final = df_temp[['País', 'Títulos']]

# Imprime a tabela até o momento
print("Versão inicial da tabela")
print(df_final)

# Remover as linhas com 0 títulos
df_final = df_final[df_final['Títulos'].str.contains('\d+')]

# Remover a última linha que traz a observação
df_final = df_final[~df_final['País'].str.contains('Em caso de empate')]

# Imprime a tabela até o momento
print("Versão tratada da tabela")
print(df_final)