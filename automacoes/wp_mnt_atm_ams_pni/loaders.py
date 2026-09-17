import pandas as pd

# Arquivos de configuração modularizados
from config import input_projeto,datalake,nrperfil,gac

def carregar_bases():
    # informação pode ser importada com um loader na pagina
    df_individuos = pd.read_csv(f'{datalake}{input_projeto}/Individuos_vivos.csv', sep=',')

    # importação realizada via Input do usuário. Automaticamente atualiza a base de GPM utilizada por processos seguinte
    df_domicilios = pd.read_excel(
        f'{datalake}{nrperfil}/NRPerfilDomicilio.xls',
        header=14
    )

    # HardCoded Base
    df_cotas_pni42 = pd.read_excel(
       f'{datalake}{input_projeto}/Cotas_PNI_BR_2025_Agrupado.xlsx', sheet_name='42RegioesPNI'
    )
    df_cotas_pni23 = pd.read_excel(
       f'{datalake}{input_projeto}/Cotas_PNI_BR_2025_Agrupado.xlsx', sheet_name='23RegioesPNI'
    )
    df_regiao = pd.read_excel(
        f'{datalake}{gac}/bs_regiões_ihs.xlsx'
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
