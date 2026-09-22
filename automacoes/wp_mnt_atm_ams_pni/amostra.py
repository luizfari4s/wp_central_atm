import numpy as np
import pandas as pd


def criar_matriz_amostra(df, fluxo):
    # ---------------------------------------------------------
    # Padronização
    # ---------------------------------------------------------    
    df = df.copy()
    df['NSE_norm'] = df['NSE_norm'].astype(str).str.strip()
    df['faixaEtaria'] = df['faixaEtaria'].astype(str).str.strip()
    df['Sexo'] = df['Sexo'].astype(str).str.strip()
    # ---------------------------------------------------------
    # NSE
    # ---------------------------------------------------------
    nse = pd.crosstab(df[fluxo], df['NSE_norm'])
    nse = nse.reindex(columns=['AB1', 'B2', 'C1', 'C2', 'DE'], fill_value=0)
    nse['TotaisNSE'] = nse[['AB1', 'B2', 'C1', 'C2', 'DE']].sum(axis=1)
    # ---------------------------------------------------------
    # Faixa etária
    # ---------------------------------------------------------
    idade = pd.crosstab(df[fluxo], df['faixaEtaria'])
    idade = idade.reindex(columns=['11-19 anos','20-29 anos','30-39 anos','40-49 anos','50 ou + anos'], fill_value=0)
    idade['TotaisFaixaEtaria'] = idade[['11-19 anos','20-29 anos','30-39 anos','40-49 anos','50 ou + anos']].sum(axis=1)
    # ---------------------------------------------------------
    # Sexo
    # ---------------------------------------------------------
    sexo = pd.crosstab(df[fluxo], df['Sexo'])
    sexo = sexo.reindex(columns=['Feminino', 'Masculino'], fill_value=0)
    sexo['totaisSexo'] = sexo[['Feminino', 'Masculino']].sum(axis=1)
    # ---------------------------------------------------------
    # Consolidar
    # ---------------------------------------------------------
    resultado = nse.join(idade).join(sexo).reset_index()
    estrutura = [fluxo,'AB1','B2','C1','C2','DE','TotaisNSE','11-19 anos','20-29 anos','30-39 anos','40-49 anos','50 ou + anos','TotaisFaixaEtaria','Feminino','Masculino','totaisSexo']
    resultado = resultado.reindex(columns=estrutura, fill_value=0)
    # ---------------------------------------------------------
    # Estrutura final
    # ---------------------------------------------------------
    colunas_numericas = [col for col in estrutura if col != fluxo]
    resultado[colunas_numericas] = resultado[colunas_numericas].fillna(0).astype(int)
    return resultado


def gap_amostral(ideal, atual, regiao):
    ideal[regiao] = ideal[regiao].str.strip()
    atual[regiao] = atual[regiao].str.strip()
    merged_df = pd.merge(ideal, atual, on=[regiao], how='left', suffixes=('_ideal', '_atual'))
    numeric_cols = ideal.select_dtypes(include=np.number).columns.tolist()
    for col in numeric_cols:
        merged_df[f'{col}_atual'] = merged_df[f'{col}_atual'].fillna(0)
    Saldo_numerico = merged_df[[f'{col}_atual' for col in numeric_cols]].values - merged_df[[f'{col}_ideal' for col in numeric_cols]].values
    Saldo = merged_df[[regiao]].copy()
    Saldo[numeric_cols] = Saldo_numerico.astype(int)
    saldoComPni = Saldo
    return saldoComPni


def construir_matrizes_e_universos(df_indiv, df_bs_domicilios, df_cotas_pni23, df_cotas_pni42):
    from wp_central_atm.automacoes.config import ORIGENS_PNI, ORIGENS_EXP

    # Amostra PNI atual:
    # PNI not null
    # Deve existir apenas 1 PNI por Domicilio
    # Há dois fluxos, um para as origens de Expansão e outro para IHS (enteno que deveria ser para as mesmmas regiões de PNI)
    matriz_amostra_pni_atual = criar_matriz_amostra(df_indiv.loc[(df_indiv.FIPanel2.notna()) & (df_indiv.idOrigem.isin(ORIGENS_PNI))], fluxo='Regioes_23_PNI')
    matriz_amostra_exp_atual = criar_matriz_amostra(df_indiv.loc[(df_indiv.FIPanel2.notna()) & (df_indiv.idOrigem.isin(ORIGENS_EXP))], fluxo='Regioes_42_EXP')


    bs_dom_universo_23_pni = df_bs_domicilios.loc[(df_bs_domicilios.FIPanel2.isna()) & (df_bs_domicilios.idOrigem.isin(ORIGENS_PNI)) & (df_bs_domicilios.NSE.notna()) & (df_bs_domicilios.Regioes_42_EXP.notna())]
    bs_dom_universo_42_exp = df_bs_domicilios.loc[(df_bs_domicilios.FIPanel2.isna()) & (df_bs_domicilios.idOrigem.isin(ORIGENS_EXP)) & (df_bs_domicilios.NSE.notna()) & (df_bs_domicilios.Regioes_42_EXP.notna())]


    bs_indiv_universo_23_pni = df_indiv.loc[(df_indiv.FIPanel2.isna()) & (df_indiv.idOrigem.isin(ORIGENS_PNI)) & (df_indiv.NSE.notna()) & (df_indiv.Regioes_42_EXP.notna()) & (df_indiv.Sexo.notna())]
    bs_indiv_universo_42_exp = df_indiv.loc[(df_indiv.FIPanel2.isna()) & (df_indiv.idOrigem.isin(ORIGENS_EXP)) & (df_indiv.NSE.notna()) & (df_indiv.Regioes_42_EXP.notna()) & (df_indiv.Sexo.notna())]


    matriz_amostra_exp_atual = matriz_amostra_exp_atual.sort_values(by='Regioes_42_EXP')
    matriz_amostra_pni_atual = matriz_amostra_pni_atual.sort_values(by='Regioes_23_PNI')


    df_cotas_pni23 = df_cotas_pni23.sort_values(by='Regioes_23_PNI')
    df_cotas_pni42 = df_cotas_pni42.sort_values(by='Regioes_42_EXP')


    gap_amostral_23_regioes = gap_amostral(df_cotas_pni23, matriz_amostra_pni_atual, 'Regioes_23_PNI')
    gap_amostral_42_regioes = gap_amostral(df_cotas_pni42, matriz_amostra_exp_atual, 'Regioes_42_EXP')

    return locals()
