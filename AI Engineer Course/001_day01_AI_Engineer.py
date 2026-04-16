#Vamos desenvolver Multi-Agent Engineer
    #crie um código para a leitura de arquivo local em python.  Arquivo c:\user\001.csv
import pandas as pd

# Define o caminho do arquivo
caminho_arquivo = r'c:\user\001.csv'

try:
    # Realiza a leitura do arquivo CSV
    df = pd.read_csv(caminho_arquivo)
    
    # Exibe as primeiras linhas para verificar a leitura
    print(df.head())
except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")
