from datetime import datetime

from carregamento import carregar_bases
from normalizacao import (
    normalizar_para_classificacao,
    preparar_masterfile,
)
from regras import (
    aplicar_rbc,
    classificar_produtos_novos,
    juntar_niveis,
    resolver_classificacao_parcial,
    separar_rbc_por_unicidade,
)


def executar_pipeline(
    rule_table_path,
    level_data_path,
    rbc_paths,
    masterfile_path,
    caminho_saida,
):
    bases = carregar_bases(
        rule_table_path=rule_table_path,
        level_data_path=level_data_path,
        rbc_paths=rbc_paths,
        masterfile_path=masterfile_path,
    )

    aux = preparar_masterfile(bases["masterfile"])

    rbc_data = separar_rbc_por_unicidade(
        bases["rbc_n1"],
        bases["rbc_n2"],
        bases["rbc_n3"],
        bases["rbc_n4"],
    )

    aux = aplicar_rbc(
        aux,
        bases["rule_table"],
    )

    merged = juntar_niveis(
        aux,
        bases["level_data"],
    )

    antigos, novos = classificar_produtos_novos(
        merged,
        rbc_data,
    )

    novos = normalizar_para_classificacao(novos)

    novos = resolver_classificacao_parcial(
        novos,
        rbc_data,
    )

    dados_finais = finalizar_resultado(
        antigos,
        novos,
    )

    exportar_resultado(
        dados_finais,
        caminho_saida,
    )

    return dados_finais


def finalizar_resultado(antigos, novos):
    dados_finais = __import__("pandas").concat(
        [antigos, novos]
    )

    dados_finais["DescUsage"] = (
        dados_finais["DescUsage"].str.title()
    )

    for coluna in [
        "NIVEL_1",
        "NIVEL_2",
        "NIVEL_3",
        "NIVEL_4",
    ]:
        dados_finais[coluna] = dados_finais[coluna].replace(
            "o",
            "",
        )

    return dados_finais


def exportar_resultado(dados_finais, caminho_saida):
    dados_finais.to_csv(
        caminho_saida,
        index=False,
        encoding="latin1",
        sep=";",
    )
