import pandas as pd
import requests
from io import StringIO
import re

url = "https://pt.wikipedia.org/wiki/Copa_Libertadores_da_Am%C3%A9rica"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)

dfs = pd.read_html(StringIO(response.text))

df_temp = dfs[11]
df_final = df_temp[['País', 'Títulos']].copy()

print("Versão inicial da tabela")
print(df_final)

# Função para extrair o número de títulos
def extrair_numero(titulo):
    match = re.search(r'(\d+)', str(titulo))  # Converter titulo para string
    if match:
        return int(match.group(1))
    else:
        return 0

# Aplicar a função à coluna 'Títulos'
df_final['Numero_Titulos'] = df_final['Títulos'].apply(extrair_numero)

# Remover as linhas com 0 títulos
df_final = df_final[df_final['Numero_Titulos'] > 0]

# Remover a última linha que traz a observação
df_final = df_final[~df_final['País'].str.contains('Em caso de empate')]

# Remover a coluna 'Numero_Titulos' se não for necessária
df_final = df_final[['País', 'Títulos']]

print("Versão tratada da tabela")
print(df_final)
