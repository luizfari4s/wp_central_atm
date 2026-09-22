
def main(dt_ref = None):
    import functions
    from os import getlogin
    from pathlib import Path
    from configparser import ConfigParser

    config = ConfigParser()

    config.read(
        Path.home() / "Documents" / "wp_central_atm" / "config.ini",
        encoding="utf-8"
)

    dl = Path.home() / config["datalake"]["caminho"]
        #import functions
 

    # Trocar para domínio interno do pc pessoal
    # dominio_interno = getlogin()

    # Pasta MASTER
    datalake = dl
    # Opção 2
    # datalake = f'C:/Users/{dominio_interno}/Numerator International/projeto-dados-ops'


    pre_aloc = functions.carregamento(
        path=f'{datalake}/do_preal_fornecedor/ref_prealoc',
        prefixo='pre'
    )
    
    trocas = {
        '{GroupId}' : 'UserPS',
        '{IndividualId}' : 'individual-id',
        '{CreationTimeStamp}' : 'created_at',
        'Origen' : 'Origen_GPM'
    }
    pre_aloc.rename(
        columns=trocas, 
        inplace=True)
    
    pre_aloc['UserPS'] = pre_aloc['UserPS'].astype(str)
    print("qty prealoca: ",pre_aloc.shape[0])

    df_cldar = functions.carregamento(
        path=f'{datalake}/do_calendario_fiscal',
        prefixo='do_cal'
        )    

    rep7 = functions.carregamento(
        path=f'{datalake}/do_rep7/bruto',
        prefixo='Brasil-Reporte-7'
    )

    rep7 = functions.normalize(rep7)
    rep7_nf = rep7.copy()

    rep7, inicio, fim = functions.filtrar_periodo_vigente(
        rep7, 
        df_cldar,
        coluna_data='DiaDeCompra',
        data_referencia=dt_ref
    )

    out = functions.inf_consolidada(
        rep7_nf,
        df_cldar,
        pre_aloc)

    functions.atualizar_consolidado(
        out,
        path_cons=f'{datalake}/do_preal_fornecedor/ref_cosolidado'
        )

    functions.atualizar_base(
        rep7, 
        inicio,
        fim, 
        path_rep7 = f'{datalake}/do_rep7/')

if __name__ == '__main__':  
    main() 