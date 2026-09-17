import pandas as pd


def selecao(gap_amostral, df_dom_universo_selecao, df_indiv_candidatos_selecao, regiao):
    df_dom_universo_selecao[regiao] = df_dom_universo_selecao[regiao].str.strip()
    df_indiv_candidatos_selecao[regiao] = df_indiv_candidatos_selecao[regiao].str.strip()
    gap_amostral[regiao] = gap_amostral[regiao].str.strip()
    df_dom_universo_selecao = df_dom_universo_selecao.loc[df_dom_universo_selecao.NSE.notna()]
    df_indiv_candidatos_selecao = df_indiv_candidatos_selecao.loc[df_indiv_candidatos_selecao.NSE.notna()]
    dom_1_candidato_23_pni = df_dom_universo_selecao.loc[df_dom_universo_selecao['faixa_candidatos'] == '1 candidato', 'iddomicilio']
    df_selecao_direta_23_exp = df_indiv_candidatos_selecao.loc[df_indiv_candidatos_selecao['iddomicilio'].isin(dom_1_candidato_23_pni)].copy()
    dom_multiplos = df_dom_universo_selecao.loc[df_dom_universo_selecao['faixa_candidatos'].isin(['2-3 candidatos','4-6 candidatos','7+ candidatos']), 'iddomicilio']
    df_candidatos_decisao = df_indiv_candidatos_selecao.loc[df_indiv_candidatos_selecao['iddomicilio'].isin(dom_multiplos)].copy()
    df_candidatos_decisao_23_pni_decisao = df_indiv_candidatos_selecao.copy()
    gap_nse = gap_amostral.set_index(regiao)
    gap_nse = gap_amostral.set_index(regiao)
    df_candidatos_decisao['gap_nse'] = [gap_nse.loc[regiao, nse] for regiao, nse in zip(df_candidatos_decisao[regiao], df_candidatos_decisao['NSE_norm'])]
    df_candidatos_decisao['gap_faixa'] = [gap_nse.loc[regiao, faixa] for regiao, faixa in zip(df_candidatos_decisao[regiao], df_candidatos_decisao['faixaEtaria'])]
    df_candidatos_decisao['gap_sexo'] = [gap_nse.loc[regiao, sexo] for regiao, sexo in zip(df_candidatos_decisao[regiao], df_candidatos_decisao['Sexo'])]
    df_candidatos_decisao['score_nse'] = -df_candidatos_decisao['gap_nse'].clip(upper=0)
    df_candidatos_decisao['score_faixa'] = -df_candidatos_decisao['gap_faixa'].clip(upper=0)
    df_candidatos_decisao['score_sexo'] = -df_candidatos_decisao['gap_sexo'].clip(upper=0)
    df_candidatos_decisao['score'] = df_candidatos_decisao['score_nse'] + df_candidatos_decisao['score_faixa'] + df_candidatos_decisao['score_sexo']
    df_candidatos_decisao['selecionado'] = 0
    idx = df_candidatos_decisao.groupby('iddomicilio')['score'].idxmax()
    df_candidatos_decisao.loc[idx, 'selecionado'] = 1
    df_indiv_candidatos_selecao['tipo_selecao'] = 'Não selecionado'
    df_indiv_candidatos_selecao.loc[df_indiv_candidatos_selecao['iddomicilio'].isin(dom_1_candidato_23_pni), 'tipo_selecao'] = 'Direto'
    df_indiv_candidatos_selecao.loc[df_indiv_candidatos_selecao.index.isin(df_candidatos_decisao.loc[df_candidatos_decisao['selecionado'] == 1].index), 'tipo_selecao'] = 'Score'
    df_selecionados_score = df_candidatos_decisao.loc[df_candidatos_decisao['selecionado'] == 1].copy()
    df_selecionados_direto = df_indiv_candidatos_selecao.loc[df_indiv_candidatos_selecao['tipo_selecao'] == 'Direto'].copy()
    df_selecao_final = pd.concat([df_selecionados_direto, df_selecionados_score], ignore_index=True)
    print('Selecionados diretos:', len(df_selecionados_direto))
    print('Selecionados por score:', len(df_selecionados_score))
    print('Total selecionado:', len(df_selecao_final))
    print('Domicílios distintos:', df_selecao_final['iddomicilio'].nunique())
    return df_selecao_final


def finalizar_selecionados(df_selecionados_23_pni, df_selecionados_42_exp):
    df_selecionados_42_exp.loc[df_selecionados_42_exp.tipo_selecao == 'Direto', 'selecionado'] = 1
    df_selecionados_23_pni.loc[df_selecionados_23_pni.tipo_selecao == 'Direto', 'selecionado'] = 1
    df_selecionados_42_exp.loc[df_selecionados_42_exp.score.notna(), 'tipo_selecao'] = 'Score'
    df_selecionados_23_pni.loc[df_selecionados_23_pni.score.notna(), 'tipo_selecao'] = 'Score'
    df_selecionados_42_exp = df_selecionados_42_exp[['iddomicilio', 'idIndividuo', 'Regioes_42_EXP', 'idOrigem', 'status_domicilio_gpm','flag_candidato', 'tipo_selecao']]
    df_selecionados_23_pni = df_selecionados_23_pni[['iddomicilio', 'idIndividuo', 'Regioes_23_PNI', 'idOrigem', 'status_domicilio_gpm','flag_candidato', 'tipo_selecao']]
    return df_selecionados_23_pni, df_selecionados_42_exp
