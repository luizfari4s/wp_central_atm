import pandas as pd

from config import (
    CORRECOES_CLASSIFICACAO,
    REGRAS_CLASSIFICACAO_PARCIAL,
    RESULTADO_CONFLITO,
    RESULTADO_HISTORICO,
    RESULTADO_PARCIAL,
    RESULTADO_PARCIAL_RESOLVIDA,
    RESULTADO_RBC,
    VALOR_NAO_CLASSIFICADO,
)


def separar_rbc_por_unicidade(rbc_n1, rbc_n2, rbc_n3, rbc_n4):
    rbcs = [rbc_n1, rbc_n2, rbc_n3, rbc_n4]
    unicos = []
    nao_unicos = []

    for rbc in rbcs:
        contagem = rbc["IdProd"].value_counts().reset_index()
        unique_ids = contagem.loc[contagem["count"] == 1, "IdProd"]

        unicos.append(
            rbc.loc[rbc["IdProd"].isin(unique_ids)].copy()
        )
        nao_unicos.append(
            rbc.loc[~rbc["IdProd"].isin(unique_ids)].copy()
        )

    not_classificable = (
        pd.concat(nao_unicos)
        .drop_duplicates(subset=["IdProd"])
        .copy()
    )
    not_classificable["IdProd"] = not_classificable["IdProd"].astype(int)

    return {
        "unique": unicos,
        "not_unique": nao_unicos,
        "not_classificable": not_classificable,
    }


def aplicar_regra(id_produto, rule_table, row):
    regra_row = rule_table.loc[
        rule_table["IdProd"] == id_produto,
        "RuleMap",
    ]

    if regra_row.empty:
        return "Sem regra no dicionário"

    regra = regra_row.values[0]
    tokens = [t.strip() for t in regra.split("+")]

    valores = [
        str(row[tok])
        for tok in tokens
        if tok in row.index and pd.notna(row[tok])
    ]

    return " ".join(valores)


def aplicar_rbc(aux, rule_table):
    aux = aux.copy()

    aux["DescUsage"] = aux.apply(
        lambda row: aplicar_regra(row["IdProd"], rule_table, row),
        axis=1,
    )

    aux["DescUsage"] = aux["DescUsage"].str.replace(
        "\u00A0", " ", regex=False
    )

    return aux


def juntar_niveis(aux, level_data):
    merged = aux.merge(
        level_data,
        on="IdArtigo",
        how="left",
    )

    merged = merged.dropna(axis=1, how="all")

    primeiras = [
        "DescUsage",
        "NIVEL_1",
        "NIVEL_2",
        "NIVEL_3",
        "NIVEL_4",
    ]

    resto = [
        coluna
        for coluna in merged.columns
        if coluna not in primeiras
    ]

    merged = merged[primeiras + resto]

    for coluna in primeiras[1:]:
        merged[coluna] = merged[coluna].fillna(
            VALOR_NAO_CLASSIFICADO
        )

    return merged


def classificar_produtos_novos(merged, rbc_data):
    novos = merged.loc[
        merged["NIVEL_1"] == VALOR_NAO_CLASSIFICADO
    ].copy()

    antigos = merged.loc[
        merged["NIVEL_1"] != VALOR_NAO_CLASSIFICADO
    ].copy()

    novos.drop(
        columns=["NIVEL_1", "NIVEL_2", "NIVEL_3", "NIVEL_4"],
        inplace=True,
    )

    for rbc in rbc_data["unique"]:
        novos = novos.merge(
            rbc,
            on="IdProd",
            how="left",
        )

    cols = [
        "DescUsage",
        "NIVEL_1",
        "NIVEL_2",
        "NIVEL_3",
        "NIVEL_4",
    ]
    resto = [c for c in novos.columns if c not in cols]
    novos = novos[cols + resto]

    for coluna in cols[1:]:
        novos[coluna] = novos[coluna].fillna(
            VALOR_NAO_CLASSIFICADO
        )

    conflito_ids = novos.loc[
        (novos["NIVEL_1"] == VALOR_NAO_CLASSIFICADO)
        & (novos["NIVEL_2"] == VALOR_NAO_CLASSIFICADO)
        & (novos["NIVEL_3"] == VALOR_NAO_CLASSIFICADO)
        & (novos["NIVEL_4"] == VALOR_NAO_CLASSIFICADO),
        "IdArtigo",
    ]

    partial_ids = novos.loc[
        novos["IdProd"].isin(
            rbc_data["not_classificable"]["IdProd"]
        ),
        "IdArtigo",
    ]

    novos["Result"] = RESULTADO_RBC
    novos.loc[
        novos["IdArtigo"].isin(partial_ids),
        "Result",
    ] = RESULTADO_PARCIAL
    novos.loc[
        novos["IdArtigo"].isin(conflito_ids),
        "Result",
    ] = RESULTADO_CONFLITO

    antigos["Result"] = RESULTADO_HISTORICO

    return antigos, novos


def buscar_valor(df, coluna, termo):
    mask = df[coluna].astype(str).str.contains(
        termo,
        case=False,
        na=False,
    )
    resultados = df.loc[mask, coluna].values

    if len(resultados) == 0:
        return VALOR_NAO_CLASSIFICADO

    return str(resultados[0])


def resolver_classificacao_parcial(
    new_products,
    rbc_data,
):
    target = new_products.copy()

    filter_pci = target.loc[
        target["Result"] == RESULTADO_PARCIAL
    ].copy()

    # Mantém exatamente o conjunto de IdProd tratado no notebook.
    for id_prod, coluna_busca in REGRAS_CLASSIFICACAO_PARCIAL.items():
        rbc_n3 = rbc_data["not_unique"][2]
        rbc_n4 = rbc_data["not_unique"][3]

        for index, row in filter_pci.iterrows():
            if (
                row["IdProd"] == id_prod
                and row["NIVEL_3"] == VALOR_NAO_CLASSIFICADO
            ):
                search_str = normalizar_texto(row[coluna_busca])

                if search_str in CORRECOES_CLASSIFICACAO:
                    target.loc[index, "NIVEL_3"] = (
                        CORRECOES_CLASSIFICACAO[search_str]
                    )
                else:
                    target.loc[index, "NIVEL_3"] = buscar_valor(
                        rbc_n3,
                        "NIVEL_3",
                        search_str,
                    )
                    target.loc[index, "NIVEL_4"] = buscar_valor(
                        rbc_n4,
                        "NIVEL_4",
                        search_str,
                    )

                target.loc[
                    index,
                    "Result",
                ] = RESULTADO_PARCIAL_RESOLVIDA

    return target


def normalizar_texto(texto):
    import unicodedata

    if pd.isna(texto):
        return texto

    return (
        unicodedata.normalize("NFKD", str(texto))
        .encode("ASCII", "ignore")
        .decode("utf-8")
        .upper()
    )
