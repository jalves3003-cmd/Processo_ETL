Projeto/
├── data/
│   ├── raw/                 # Coloque seus CSVs do INEP aqui (2020 a 2025)
│   └── processed/           # Onde o arquivo final limpo será salvo
├── src/
│   ├── __init__.py
│   ├── config_etl.py        # Configurações (Nomes das colunas, Caminhos)
│   ├── censo_processor.py   # O "Worker": Limpa UM arquivo individual
│   └── etl_pipeline.py      # O "Gerente": Junta todos os anos
└── main_etl.py              # O arquivo que você executa