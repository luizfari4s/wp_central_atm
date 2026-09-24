from datetime import datetime

import pandas as pd

from config import output_projeto,datalake

def gerar_saida(df_selecionados_23_pni, df_selecionados_42_exp, gap_amostral_23_regioes, gap_amostral_42_regioes):
    df_lista_importacao = pd.concat([df_selecionados_23_pni[['idIndividuo']], df_selecionados_42_exp[['idIndividuo']]])
    df_lista_importacao['painel'] = 2
    data = datetime.now().strftime('%d%m%Y')
    fn = f'{output_projeto}'
    nm = f'/PROD_SELECAO_PNI_teste_{data}.xlsx'
    with pd.ExcelWriter(f'{fn}{nm}', engine='openpyxl') as writer:
        df_lista_importacao.to_excel(writer, sheet_name='Lista Para Importação', index=False)
        df_selecionados_23_pni.to_excel(writer, sheet_name='Detalhe 23 PNI', index=False)
        df_selecionados_42_exp.to_excel(writer, sheet_name='Detalhe 42 EXP', index=False)
        gap_amostral_23_regioes.to_excel(writer, sheet_name='Gap Amostral 23 PNI', index=False)
        gap_amostral_42_regioes.to_excel(writer, sheet_name='Gap Amostral 42 EXP', index=False)
    print(f'Arquivo gerado com sucesso: {fn + nm}')
    return fn + nm
