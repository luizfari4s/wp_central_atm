import pandas as pd
import unicodedata

from config_1 import (
    ATIVOS_EXCLUIDOS,
    COLUNAS_DESCARTAR,
    NORMALIZACOES_EXATAS,
    SUB_EXCLUIDOS,
    VALORES_AUSENTES,
)


def normalizar_texto(texto):
    if pd.isna(texto):
        return texto

    texto = (
        unicodedata.normalize("NFKD", str(texto))
        .encode("ASCII", "ignore")
        .decode("utf-8")
    )
    return texto.upper()


def preparar_masterfile(aux):
    aux = aux.copy()
    aux["DescUsage"] = None

    aux.drop(columns=COLUNAS_DESCARTAR, inplace=True)

    for coluna, valores in VALORES_AUSENTES.items():
        if coluna in aux.columns:
            for valor in valores:
                aux[coluna] = aux[coluna].str.replace(
                    valor, "", regex=False
                )

    if "Producto" in aux.columns:
        for origem, destino in NORMALIZACOES_EXATAS.items():
            aux["Producto"] = aux["Producto"].str.replace(
                origem, destino, regex=False
            )

    if "Contenido" in aux.columns:
        mask_ml = aux["Contenido"].str.contains("ML", na=False)
        aux.loc[mask_ml, "Contenido"] = (
            aux.loc[mask_ml, "Contenido"] + " STR_CHANGE_ML"
        )

        mask_gr = aux["Contenido"].str.contains("GR", na=False)
        aux.loc[mask_gr, "Contenido"] = (
            aux.loc[mask_gr, "Contenido"] + " STR_CHANGE_GR"
        )

        aux["Contenido"] = aux["Contenido"].str.replace(
            "ML ", "", regex=False
        )
        aux["Contenido"] = aux["Contenido"].str.replace(
            "GR ", "", regex=False
        )
        aux["Contenido"] = aux["Contenido"].str.replace(
            "STR_CHANGE_ML", "ml", regex=False
        )
        aux["Contenido"] = aux["Contenido"].str.replace(
            "STR_CHANGE_GR", "gr", regex=False
        )

    aux.drop(columns={"Creado", "Fuente"}, inplace=True, errors="ignore")

    if "Sub" in aux.columns:
        aux = aux.loc[
            ~aux["Sub"].isin(SUB_EXCLUIDOS)
        ]

    if "Activo" in aux.columns:
        aux = aux.loc[
            ~aux["Activo"].isin(ATIVOS_EXCLUIDOS)
        ]

    return aux


def normalizar_para_classificacao(df):
    df = df.copy()

    if "Sub" in df.columns:
        df["Sub"] = df["Sub"].apply(normalizar_texto)

    if "Producto" in df.columns:
        df["Producto"] = df["Producto"].apply(normalizar_texto)

    return df
