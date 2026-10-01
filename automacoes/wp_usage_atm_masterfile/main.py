from pathlib import Path

from pipeline import executar_pipeline

from config_1 import rbc_path,input_projeto, output_projeto
def main(
    rule_table_path,
    level_data_path,
    rbc_paths,
    masterfile_path,
    caminho_saida,
):
    """
    Ponto de entrada da automação Stage Area.

    O orquestrador fornece os arquivos.
    Esta função executa o processo completo.
    """
    return executar_pipeline(
        rule_table_path=rule_table_path,
        level_data_path=level_data_path,
        rbc_paths=rbc_paths,
        masterfile_path=masterfile_path,
        caminho_saida=caminho_saida,
    )


# Alias explícito para uso pela Central.
processar_stage_area = main


if __name__ == "__main__":
    # Exemplo de execução local.
    # Na Central, o esperado é chamar main(...) diretamente.
    BASE = Path(".")
    main(
        rule_table_path=str(rbc_path) + "/rule_table_with_rulemap_v2.csv",
        level_data_path=str(rbc_path) + "/level_data.CSV",
        rbc_paths={
            "N1": str(rbc_path) + "/RBC_N1.CSV",
            "N2": str(rbc_path) + "/RBC_N2.CSV",
            "N3": str(rbc_path) + "/RBC_N3.CSV",
            "N4": str(rbc_path) + "/RBC_N4.CSV",
        },
        masterfile_path=str(input_projeto) + "/MF_Atual.CSV",
        caminho_saida=str(output_projeto) + "/MF_BR_USAGE_teste.csv",
    )
