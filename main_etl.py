from src.etl_piperline import EltPiperline

if __name__ == "__main__":
    print("=== MODULO ETL (CENSO ESCOLAR) ===")

    piperline = EltPiperline()
    piperline.executar()
    piperline.filtrar_e_salvar()

    print("=== FIM DO MODULO ===") 