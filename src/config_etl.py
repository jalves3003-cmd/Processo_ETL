import os

# Caminhos
DIR_RAW = os.path.join('data', 'raw')
DIR_PROCESSED = os.path.join('data','processed')

# Arquivos de entrada
# Chave = Ano, valor = Nome do arquivo na pasta data/raw

ARQUIVOS_ENTRADA = {
    2025: 'dados_2025.xlsx',
    2024: 'dados_2024.xlsx', 
    2023: 'dados_2023.xlsx',
    2022: 'dados_2022.xlsx',
    2021: 'dados_2021.xlsx',
    2020: 'dados_2020.xlsx',
}

# Filtros
MUNICIPIO_ALVO = "FORTALEZA"

# Definição das colunas (Baseado no laout visualizado do arquivo)
COLUNAS_MAPEAMENTO = [
    'Lixo', 'Descrição', 
    'Creche_parcial', 'Creche_Integral',
    'Pre_Parcial', 'Pre_Integral', 
    'Fund_Iniciais_Parcial', 'Fund_Iniciais_Integral',
    'Fund_Finais_Parcial', 'Medio_Integral',
    'EJA_Fund', 'EJA_Medio' 
]

# Colunas safadinhas que queremos manter no final
COLUNAS_FINAIS = [
    'Ano', 'Municipio', 'Dependencia_Administrativa',
    'Creche_Parcial', 'Creche_Integral', 
    'Pre_Parcial', 'Pre_Integral', 
    'Fund_Iniciais_Parcial', 'Fund_Iniciais_Integral', 
    'Fund_Finais_Parcial', 'Fund_Finais_Integral', 
    'Medio_Parcial', 'Medio_Integral', 
    'EJA_Fund', 'EJA_Medio'
]