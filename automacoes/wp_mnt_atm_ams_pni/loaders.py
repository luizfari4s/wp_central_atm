import pandas as pd

# Arquivos de configuração modularizados
from config import input_projeto,datalake,nrperfil,gac

def carregamento(prefixo, path, hd=None,fluxo_externo=False,sh=None):
    import pandas as pd
    import glob
    import os

    arquivos = (
        glob.glob(os.path.join(path, f"{prefixo}*.csv"))
        + glob.glob(os.path.join(path, f"{prefixo}*.xlsx"))
        + glob.glob(os.path.join(path, f"{prefixo}*.xls"))
    )

    dfs = []

    for arq in arquivos:

        extensao = os.path.splitext(arq)[1].lower()

        if extensao == ".csv":
            df = pd.read_csv(arq, sep=';', low_memory=False)

        elif extensao in [".xlsx", ".xls"]:

            if sh is not None:
                df = pd.read_excel(arq, sheet_name=sh)

            elif hd is not None:
                df = pd.read_excel(arq, header=hd)

            else:
                df = pd.read_excel(arq)
        else:
            continue

        # Sempre guarda a origem
        df['arquivo_origem'] = os.path.basename(arq)

        dfs.append(df)

    if not dfs:
        raise ValueError("Nenhum arquivo encontrado para o prefixo informado.")

    df_final = pd.concat(dfs, ignore_index=True)

    # Remove apenas no fluxo externo
    if fluxo_externo:
        df_final.drop(columns='arquivo_origem', inplace=True)

    return df_final

def carregar_bases():
    # informação pode ser importada com um loader na pagina
    df_individuos = pd.read_csv(f'{input_projeto}/Individuos_vivos.csv', sep=',')

    # importação realizada via Input do usuário. Automaticamente atualiza a base de GPM utilizada por processos seguinte
    df_domicilios = carregamento(
        path= nrperfil,
        prefixo='NRPerfilDomicilio',
        hd=14
    )
    # HardCoded Base
    df_cotas_pni42 = pd.read_excel(
       f'{input_projeto}/Cotas_PNI_BR_2025_Agrupado.xlsx', sheet_name='42RegioesPNI'
    )
    df_cotas_pni23 = pd.read_excel(
       f'{input_projeto}/Cotas_PNI_BR_2025_Agrupado.xlsx', sheet_name='23RegioesPNI'
    )
    df_regiao = pd.read_excel(
        f'{gac}/bs_regiões_ihs.xlsx'
    )

    # lista de dataframes
    return {
        'df_individuos': df_individuos,
        'df_domicilios': df_domicilios,
        'df_cotas_pni42': df_cotas_pni42,
        'df_cotas_pni23': df_cotas_pni23,
        'df_regiao': df_regiao,
    }

def preparar_bases_carregadas(bases):
    df_individuos = bases['df_individuos']
    df_domicilios = bases['df_domicilios']
    df_cotas_pni42 = bases['df_cotas_pni42']
    df_cotas_pni23 = bases['df_cotas_pni23']
    df_regiao = bases['df_regiao']

    df_cotas_pni42.drop(columns=['PAIS','gacodeIdeal'], inplace=True)
    df_cotas_pni42.rename(columns={'REGIÃO':'Regioes_42_EXP'}, inplace=True)
    df_cotas_pni42.drop(columns='REGIAO_LAST', inplace=True)
    df_cotas_pni23.rename(columns={'REGIÃO':'Regioes_23_PNI'}, inplace=True)
    df_individuos.rename(columns={'idDomicilio':'iddomicilio', 'painel_2':'FIPanel2'}, inplace=True)

    return df_individuos, df_domicilios, df_cotas_pni42, df_cotas_pni23, df_regiao
