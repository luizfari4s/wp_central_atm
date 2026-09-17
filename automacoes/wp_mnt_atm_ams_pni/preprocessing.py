import re
import unicodedata

import numpy as np
import pandas as pd


def normalizar_texto(valor):
    if pd.isna(valor):
        return None
    valor = str(valor)
    valor = ''.join(c for c in valor if unicodedata.category(c) not in ('Cc', 'Cf'))
    valor = unicodedata.normalize('NFKC', valor)
    valor = valor.replace('\xa0', ' ')
    valor = valor.replace('\u200b', '')
    valor = valor.replace('\ufeff', '')
    valor = re.sub(r'\s+', ' ', valor)
    valor = valor.strip()
    return valor


def preparar_domicilios(df_domicilios, df_individuos, df_regiao):
    # Identificar a amostra viva pertencente ao PNC

    # Cruzamento com a base da amostra PNI via left jpjoin.
    df_bs_domicilios = df_domicilios.merge(
        df_individuos.loc[df_individuos.FIPanel2.notna()][['iddomicilio', 'FIPanel2']],
        on='iddomicilio', how='left'
    )

    df_bs_domicilios = df_bs_domicilios[['iddomicilio','FIPanel1','FIPanel2','GAC','NSE', 'Origen Hogar']].copy()

    df_bs_domicilios = df_bs_domicilios.merge(
        df_regiao[['GACODE_KANTAR_Nuevo','Região Expansão 2024','Região Kantar PNI 23 regiones']],
        left_on='GAC', right_on='GACODE_KANTAR_Nuevo', how='left'
    )

    df_bs_domicilios.drop(columns=['GAC'], inplace=True)

    df_bs_domicilios.rename(columns={
        'Região Expansão 2024': 'Regioes_42_EXP',
        'Região Kantar PNI 23 regiones': 'Regioes_23_PNI'
    }, inplace=True)

    
    df_bs_domicilios['NSE'] = df_bs_domicilios['NSE'].replace({'B1':'AB1', 'A':'AB1'})
    df_bs_domicilios['Origen Hogar'] = df_bs_domicilios['Origen Hogar'].apply(normalizar_texto)

    map_origem = {
        'Expansión Nordeste': {'origem_antiga': '20 - Expansão Nordeste', 'idOrigem': 20},
        'Expansión Centro-Oeste': {'origem_antiga': '22 - Expansão Centro-Oeste', 'idOrigem': 22},
        'Expansión Interior SP': {'origem_antiga': '21 - Expansão Interior SP', 'idOrigem': 21},
        'Expansión Resto BR': {'origem_antiga': '23 - Expansão Resto BR', 'idOrigem': 23},
        'IBS': {'origem_antiga': '1 - IBS', 'idOrigem': 1},
        'Golondrina': {'origem_antiga': '16 - Migrado Golondrina BR', 'idOrigem': 16},
        'Golondrina Nuevo Reclutado BR': {'origem_antiga': '18 - Golondrina Nuevo Reclutado BR', 'idOrigem': 18},
        'Mirror Migrado': {'origem_antiga': '2 - Mirror Migrado', 'idOrigem': 2},
        'Mirror Nuevo Referido': {'origem_antiga': '3 - Mirror Nuevo Referido', 'idOrigem': 3},
        'Mirror Nuevo Reclutado': {'origem_antiga': '4 - Mirror Nuevo Reclutado', 'idOrigem': 4}
    }
    df_bs_domicilios['origem'] = df_bs_domicilios['Origen Hogar'].map(lambda x: map_origem.get(x, {}).get('origem_antiga'))
    df_bs_domicilios['idOrigem'] = df_bs_domicilios['Origen Hogar'].map(lambda x: map_origem.get(x, {}).get('idOrigem'))
    return df_bs_domicilios


def preparar_individuos(df_individuos, df_bs_domicilios):
    df_indiv = df_individuos[['iddomicilio', 'idIndividuo','Sexo','Idade','DonadeCasa','NSE','FIPanel2']].copy()
    map_nse = {1:'AB1', 2:'AB1', 3:'B2', 4:'C1', 5:'C2', 6:'DE'}
    df_indiv['NSE_norm'] = df_indiv['NSE'].map(map_nse)
    df_indiv.Sexo = df_indiv.Sexo.map({'Female': 'Feminino', 'Male': 'Masculino'})
    bins = [11, 20, 30, 40, 50, np.inf]
    labels = ['11-19 anos', '20-29 anos', '30-39 anos','40-49 anos', '50 ou + anos']
    df_indiv['faixaEtaria'] = pd.cut(df_indiv['Idade'], bins=bins, labels=labels, right=False)
    df_indiv = df_indiv.merge(df_bs_domicilios[['iddomicilio','Regioes_42_EXP','Regioes_23_PNI','Origen Hogar','idOrigem']], on='iddomicilio', how='left')
    df_indiv.Idade = df_indiv.Idade.fillna(0).astype(int)
    df_mono = df_indiv.groupby('iddomicilio')['idIndividuo'].count().reset_index()
    df_mono = df_mono.loc[df_mono.idIndividuo == 1]
    df_mono.rename(columns={'idIndividuo':'mono_indiv'}, inplace=True)
    df_indiv = df_indiv.merge(df_mono, on='iddomicilio', how='left')
    df_indiv.mono_indiv = df_indiv.mono_indiv.fillna(0)
    df_indiv.mono_indiv = df_indiv.mono_indiv.astype(bool)
    df_indiv['status_domicilio_gpm'] = df_indiv.iddomicilio.isin(df_bs_domicilios.iddomicilio)
    df_indiv = df_indiv.loc[df_indiv.status_domicilio_gpm == True]
    df_indiv.DonadeCasa = df_indiv.DonadeCasa.astype(bool)
    lista_domicilio_pni = df_bs_domicilios.loc[df_bs_domicilios.FIPanel2.notna()].iddomicilio
    df_indiv['lar_pni'] = df_indiv.iddomicilio.isin(lista_domicilio_pni)
    return df_indiv
