# 📊 MÓDULO ETL - CENSO ESCOLAR (PROJETO FINAL)

## 📌 Visão Geral
Este módulo é responsável pela **Extração, Transformação e Carga (ETL)** dos dados educacionais. 

O objetivo é processar os relatórios "semi-estruturados" do Censo Escolar (disponibilizados pelo INEP via Diário Oficial) e transformá-los em um dataset limpo, padronizado e filtrado para o município de **Fortaleza**, abrangendo a série histórica de **2020 a 2025**.

---

## 📂 Arquitetura dos Arquivos
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

O código foi organizado seguindo o princípio de separação de responsabilidades. Abaixo, a explicação detalhada de cada componente:

### 1. `main_etl.py` (O Gatilho)
* **Função:** É o ponto de entrada da aplicação.
* **O que faz:** Inicializa a pipeline e dispara a execução. É o único arquivo que você precisa executar no terminal para rodar todo o processo.

### 2. `src/config_etl.py` (As Regras)
* **Função:** Arquivo de configuração centralizada.
* **O que faz:** * Define os caminhos das pastas (`data/raw`, `data/processed`).
    * Mapeia os nomes dos arquivos de entrada por ano.
    * Lista as colunas que devem ser lidas e seus nomes finais.
    * Define os filtros globais (ex: `MUNICIPIO_ALVO = "FORTALEZA"`).
* **Por que é útil:** Se o layout do arquivo do governo mudar ano que vem, basta ajustar este arquivo sem quebrar o código lógico.

### 3. `src/censo_processor.py` (O Operário)
* **Função:** Classe responsável por limpar **um único arquivo** csv/excel.
* **O que faz (A Mágica da Limpeza):**
    * Lê o arquivo bruto ignorando cabeçalhos de texto inúteis.
    * **Tratamento de Estrutura:** Resolve o problema do layout do INEP onde o nome do município aparece como um título de seção e não como coluna. Utiliza a técnica de *Forward Fill* (`ffill`) para propagar o nome do município para as linhas de dados.
    * Padroniza nomes (maiúsculas, remoção de acentos).
    * Converte colunas numéricas, tratando erros de formatação.

### 4. `src/etl_pipeline.py` (O Gerente)
* **Função:** Orquestrador do processo em lote (Batch Processing).
* **O que faz:**
    * Itera sobre todos os anos definidos no `config_etl.py`.
    * Instancia um `CensoProcessor` para cada ano.
    * Consolida (junta) todos os DataFrames anuais em um único "Tabelão".
    * Aplica o filtro final por Município.
    * Salva o resultado em `data/processed/censo_escolar_tratado.csv`.

---

## 🛠️ Como Executar

1.  Certifique-se de que os arquivos brutos do INEP (ex: `dou_finalr_anexo_I_2025.csv`) estejam na pasta `data/raw/`.
2.  No terminal, execute:

```bash
python main_etl.py