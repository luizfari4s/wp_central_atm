from amostra import construir_matrizes_e_universos
from eligibilidade import construir_universos, percentuais_universo
from loaders import carregar_bases, preparar_bases_carregadas
from outputs import gerar_saida
from preprocessing import preparar_domicilios, preparar_individuos
from selecao import finalizar_selecionados, selecao
from wp_central_atm.automacoes.config import ORIGENS_PNI, ORIGENS_EXP


def main():
    bases = carregar_bases()
    df_individuos, df_domicilios, df_cotas_pni42, df_cotas_pni23, df_regiao = preparar_bases_carregadas(bases)

    df_bs_domicilios = preparar_domicilios(df_domicilios, df_individuos, df_regiao)
    df_indiv = preparar_individuos(df_individuos, df_bs_domicilios)

    estruturas = construir_matrizes_e_universos(df_indiv, df_bs_domicilios, df_cotas_pni23, df_cotas_pni42)
    gap_amostral_23_regioes = estruturas['gap_amostral_23_regioes']
    gap_amostral_42_regioes = estruturas['gap_amostral_42_regioes']

    universos = construir_universos(
        estruturas['bs_indiv_universo_23_pni'], estruturas['bs_dom_universo_23_pni'],
        estruturas['bs_indiv_universo_42_exp'], estruturas['bs_dom_universo_42_exp']
    )
    df_dom_universo_selecao_23_pni = universos['df_dom_universo_selecao_23_pni']
    df_indiv_candidatos_selecao_23_pni = universos['df_indiv_candidatos_selecao_23_pni']
    df_dom_universo_selecao_42_exp = universos['df_dom_universo_selecao_42_exp']
    df_indiv_candidatos_selecao_42_exp = universos['df_indiv_candidatos_selecao_42_exp']

    df_perc_universo_42_exp, df_perc_universo_23_pni = percentuais_universo(
        df_dom_universo_selecao_42_exp, df_dom_universo_selecao_23_pni
    )

    total_geral = estruturas['bs_dom_universo_42_exp'][estruturas['bs_dom_universo_42_exp'].FIPanel2.isna()].iddomicilio.nunique() + estruturas['bs_dom_universo_23_pni'][estruturas['bs_dom_universo_23_pni'].FIPanel2.isna()].iddomicilio.nunique()
    total_painel_PNI = estruturas['bs_dom_universo_23_pni'][estruturas['bs_dom_universo_23_pni'].FIPanel2.isna()].iddomicilio.nunique()
    total_painel_EXP = estruturas['bs_dom_universo_42_exp'][estruturas['bs_dom_universo_42_exp'].FIPanel2.isna()].iddomicilio.nunique()
    print('Total de indivíduos não participantes do PNI: ', total_geral)
    print('Total de candidatos do Expansão (sem aplicação da regra): ', total_painel_EXP)
    print('Total de candidatos do PNI (sem aplicação da regra): ', total_painel_PNI)
    print('\nProporção de candidados por Universo (42 Expansão): \n')
    print(df_perc_universo_42_exp)
    print('\nProporção de candidados por Universo (23 PNI): \n')
    print(df_perc_universo_23_pni)

    df_selecionados_23_pni = selecao(gap_amostral_23_regioes, df_dom_universo_selecao_23_pni, df_indiv_candidatos_selecao_23_pni, 'Regioes_23_PNI')

    df_selecionados_42_exp = selecao(gap_amostral_42_regioes, df_dom_universo_selecao_42_exp, df_indiv_candidatos_selecao_42_exp, 'Regioes_42_EXP')
    
    df_selecionados_23_pni, df_selecionados_42_exp = finalizar_selecionados(df_selecionados_23_pni, df_selecionados_42_exp)

    return gerar_saida(df_selecionados_23_pni, df_selecionados_42_exp, gap_amostral_23_regioes, gap_amostral_42_regioes)


if __name__ == '__main__':
    main()
