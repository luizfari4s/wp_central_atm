from pathlib import Path
from datetime import datetime
import sys
from os import getlogin

# Raiz do projeto wp_central_atm
ROOT = Path(__file__).resolve().parent.parent

PATH_AUTOMACOES = ROOT / "automacoes"

PATH_ATOS = (
    PATH_AUTOMACOES /
    "wp_rct_atm_atos_tc"
)

PATH_VALIDACAO = (
    PATH_AUTOMACOES /
    "wp_rct_atm_val_ficha_tc"
)


for path in [
    PATH_AUTOMACOES,
    PATH_ATOS,
    PATH_VALIDACAO
]:

    if str(path) not in sys.path:

        sys.path.insert(
            0,
            str(path)
        )

from wp_rct_atm_atos_tc.main import main as atualizar_atos

from wp_rct_atm_val_ficha_tc.main import main as validacao_fichas

def flx_2(data_corte=None):
    # data_corte é utilizado para processos de fechamento e reprocessamento de bases

    print(f"[{datetime.now()}] [INFO] [ATOS] Processamento da base de ATOS")
    atualizar_atos(data_corte)

    validacao_fichas()


def preparar_input_ficha(
    arquivo,
    pasta_destino= f'C:/Users/{getlogin()}/Numerator International/BKO - Documents/projeto-dados-ops//do_ficha/tc/input_bruto'
):

    pasta_destino = Path(pasta_destino)

    # Garante que a pasta existe
    pasta_destino.mkdir(
        parents=True,
        exist_ok=True
    )

    # Remove arquivos antigos
    for item in pasta_destino.iterdir():

        if item.is_file():

            item.unlink()

    # Define destino
    destino = pasta_destino / arquivo.name

    # Salva o novo arquivo
    with open(destino, "wb") as f:

        f.write(arquivo.getbuffer())

    return destino
















