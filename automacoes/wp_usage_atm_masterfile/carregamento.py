from pathlib import Path
import pandas as pd


def ler_csv(caminho):
    return pd.read_csv(
        caminho,
        sep=";",
        encoding="latin1",
        low_memory=False,
    )


def carregar_bases(
    rule_table_path,
    level_data_path,
    rbc_paths,
    masterfile_path,
):
    rule_table = ler_csv(rule_table_path)
    rule_table.rename(
        columns={
            "DESCRIPCIÓN DEL PRODUCTO": "DescRule",
            "DESCRIÇÃO USAGE": "OutputDesc",
            "IdProduto": "IdProd",
        },
        inplace=True,
    )

    level_data = ler_csv(level_data_path)

    rbc_n1 = ler_csv(rbc_paths["N1"])
    rbc_n2 = ler_csv(rbc_paths["N2"])
    rbc_n3 = ler_csv(rbc_paths["N3"])
    rbc_n4 = ler_csv(rbc_paths["N4"])

    masterfile = ler_csv(masterfile_path)

    return {
        "rule_table": rule_table,
        "level_data": level_data,
        "rbc_n1": rbc_n1,
        "rbc_n2": rbc_n2,
        "rbc_n3": rbc_n3,
        "rbc_n4": rbc_n4,
        "masterfile": masterfile,
    }
