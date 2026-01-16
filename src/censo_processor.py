import pandas as pd
import numpy as np
import os
from src.config_etl import COLUNAS_MAPEAMENTO, COLUNAS_FINAIS, DIR_RAW

class CensoProcessor:
    def __init__(self, ano, nome_arquivo):
        self.ano = ano
        self.caminho = os.path.join(DIR_RAW, nome_arquivo)
        self.df = None
    
    def carregar_arquivos(self):
        """
        Lê o CSV ignorando as linhas iniciasis de metadados
        """

        encodings = ['utf-8', 'latin1', 'ISO-8859-1']

        for enc in encodings:
            try:
                #skiprows = 10 pula o cabeçalho de texto do PDF
                self.df = pd.read_csv(
                    self.caminho,
                    header = None, 
                    skiprows=10,
                    sep=',',
                    encoding=enc,       # Tenta o encoding da vez
                    engine='python',    # Mais lento, porém mais robusto contra erros
                    on_bad_lines='skip' # Pula linhas quebradas sem travar o script
                    )

                ## Se leu, precisamos garantir que não pegamos colunas vazias extras à direita
                # O arquivo pode ter vindo com colunas a mais (ex: 20 colunas, mas só usamos 14)
                if self.df.shape[1] > len(COLUNAS_MAPEAMENTO):
                    self.df = self.df.iloc[:, :len(COLUNAS_MAPEAMENTO)]
                
                # Atribui os nomes das colunas
                self.df.columns = COLUNAS_MAPEAMENTO
                
                print(f"   ✅ Arquivo {self.ano} carregado! (Enc: {enc} | Linhas: {len(self.df)})")
                return # Sucesso!
            
            except Exception as e:
                # Se der erro neste encoding, tenta o próximo silenciosamente
                continue
        
        # Se chegou aqui, falhou em todos
        print(f"   ❌ ERRO CRÍTICO: Não foi possível ler o arquivo {self.caminho}")
        self.df = pd.DataFrame()

    def tratar_estrutura(self):
        """
        Aplica gostosinho a lógica de Forward Fill para corrigir os municipios
        """
        if self.df.empty: return

        # Lógica: Se a coluna de dados for NaN, a linha é um Cabeçalho de Municipio
        self.df['Eh_Municipio'] = self.df['Creche_Parcial'].isna()

        # Copia o nome do municipio para uma nova coluna
        self.df['Municipio'] = self.df['Municipio'].ffill()

        #Preenche para baixo (ffill)
        self.df['Municipio'] = self.df[~self.df['Eh_Municipio']].copy()

        # Remove linhas vazias/lixo
        self.df = self.df.dropna(subset=['descricao'])
    
    def padronizar_dados(self):
        """
        Converte tipos, adiciona ano e limpa strings
        """
        if self.df.empty: return

        # Adiciona a linha mais pedofila de todas, a coluna ano
        self.df['Ano'] = self.ano

        # Renomeia coluna de descrição (Que agora é só tipo de escola)
        self.df = self.df.rename(columns={'Descricao': 'Dependencia_Administrativa'})

        #Padroniza texto para facilitar filtros
        self.df['Municipio'] = self.df['Municipio'].astype(str).str.upper().str.strip()

        # Converte colunas numéricas (tira pontos se houver e transforma em int/float)
        cols_num = [c for c in COLUNAS_FINAIS if c not in ['Ano', 'Municipio', 'Dependencia_Administrativa']]
        for col in cols_num:
            # 'errors = coerce' transforma erros em NaN, fillna(0) transforma NaN em 0
            self.df[col] = pd.to_numeric(self.df[col], errors = 'coerce').fillna(0)
        
        # Filtra apenas as colunas úteis
        self.df = self.df[COLUNAS_FINAIS]

    def get_dados(self):
        return self.df