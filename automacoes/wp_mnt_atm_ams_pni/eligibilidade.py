import numpy as np
import pandas as pd


def candidatos_reais(df_indiv_filtrado_origem, df_bs_domicilios_filtrado_origem):
    df_candidatos = df_indiv_filtrado_origem.loc[df_indiv_filtrado_origem.lar_pni == False]
    df_candidatos['flag_candidato'] = np.select(
        [
            (df_candidatos.Idade >= 11) & (df_candidatos.DonadeCasa == False),
            (df_candidatos.Idade >= 11) & (df_candidatos.DonadeCasa == True) & (df_candidatos.mono_indiv == True),
            (df_candidatos.Idade < 11),
        ],
        [
            'Individuo do lar > 11 anos',
            'Dona de casa do lar > 11 anos E mono_indi',
            'individuo do lar < 11 anos'
        ],
        default='Exclusão por regra'
    )
    df_bs_universo_domicilios_not_pni = df_bs_domicilios_filtrado_origem
    flt = ['Dona de casa do lar > 11 anos E mono_indi', 'Individuo do lar > 11 anos']
    candidatos_regras = df_candidatos.loc[df_candidatos.flag_candidato.isin(flt)]
    df_candidatos_reais = candidatos_regras.groupby('iddomicilio')['idIndividuo'].count().reset_index()
    df_candidatos_reais.rename(columns={'idIndividuo':'candidatos_reais'}, inplace=True)
    df_bs_universo_domicilios_not_pni = df_bs_universo_domicilios_not_pni.merge(df_candidatos_reais, on='iddomicilio', how='left')
    df_bs_universo_domicilios_not_pni['candidatos_reais'] = df_bs_universo_domicilios_not_pni['candidatos_reais'].fillna(0)
    bins = [-1, 0, 1, 3, 6, float('inf')]
    labels = ['0 candidatos','1 candidato','2-3 candidatos','4-6 candidatos','7+ candidatos']
    df_bs_universo_domicilios_not_pni['faixa_candidatos'] = pd.cut(df_bs_universo_domicilios_not_pni['candidatos_reais'], bins=bins, labels=labels, include_lowest=True)
    return df_bs_universo_domicilios_not_pni, candidatos_regras


def construir_universos(bs_indiv_universo_23_pni, bs_dom_universo_23_pni, bs_indiv_universo_42_exp, bs_dom_universo_42_exp):
    df_dom_universo_selecao_23_pni, df_indiv_candidatos_selecao_23_pni = candidatos_reais(bs_indiv_universo_23_pni, bs_dom_universo_23_pni)
    df_dom_universo_selecao_42_exp, df_indiv_candidatos_selecao_42_exp = candidatos_reais(bs_indiv_universo_42_exp, bs_dom_universo_42_exp)
    return locals()


def percentuais_universo(df_dom_universo_selecao_42_exp, df_dom_universo_selecao_23_pni):
    ordem = ['0 candidatos','1 candidato','2-3 candidatos','4-6 candidatos','7+ candidatos']
    df_dom_universo_selecao_42_exp['faixa_candidatos'] = pd.Categorical(df_dom_universo_selecao_42_exp['faixa_candidatos'], categories=ordem, ordered=True)
    df_perc_universo_42_exp = (df_dom_universo_selecao_42_exp['faixa_candidatos'].value_counts(dropna=False, sort=False).to_frame('qtd').assign(proporcao=lambda x: x['qtd'] / x['qtd'].sum() * 100).reset_index())
    df_perc_universo_23_pni = (df_dom_universo_selecao_23_pni['faixa_candidatos'].value_counts(dropna=False, sort=False).to_frame('qtd').assign(proporcao=lambda x: x['qtd'] / x['qtd'].sum() * 100).reset_index())
    return df_perc_universo_42_exp, df_perc_universo_23_pni
