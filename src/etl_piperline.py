import pandas as pd
import os
from src.censo_processor import CensoProcessor
from src.config_etl import ARQUIVOS_ENTRADA, MUNICIPIO_ALVO, DIR_PROCESSED

class EltPiperline:
    def __init__(self):
        self.dados_consolidados = pd.DataFrame()

    def executar(self):
        listas_dfs = []

        print("Iniciando Pipeline de Processamento ...")
        for ano, arquivo in ARQUIVOS_ENTRADA.items():
            processador = CensoProcessor(ano, arquivo)
            processador.carregar_arquivos()
            processador.tratar_estrutura()
            processador.padronizar_dados()

            df_ano = processador.get_dados()

            if not df_ano.empty:
                listas_dfs.append(df_ano)
        
        if listas_dfs:
            self.dados_consolidados = pd.concat(listas_dfs, ignore_index = True)
            print(f"Total de registros processados: {len(self.dados_consolidados)}")
        else:
            print("Sobrou nd pro beta, nenhum dado foi processado.")

    def filtrar_e_salvar(self):
        if self.dados_consolidados.empty:
            return
        
        df_final = self.dados_consolidados.copy()

        # Aplica filtro de municipio
        print(f"filtrando por: {MUNICIPIO_ALVO}")
        # Filtra onde o municipio CONTÉM o nome alvo (segurança contra espaços extras)
        df_final = df_final['Municipio'].str.contains(MUNICIPIO_ALVO, na = False)

        caminho_saida = os.path.join(DIR_PROCESSED, 'censo_escolar_tratado.csv')
        df_final.to_csv(caminho_saida, index = False, encoding= 'utf-8-sig')

        print(f"SUCESSO!! Arquivo salvo em: {caminho_saida}")
        print("\nAmostra dos dados:")
        print(df_final.head())
        