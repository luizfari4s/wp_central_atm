from pathlib import Path
from datetime import datetime
import sys
from os import getlogin

# Raiz do projeto wp_central_atm
ROOT = Path(__file__).resolve().parent.parent

PATH_AUTOMACOES = ROOT / "automacoes"

PATH_LEV_PNI = (
    PATH_AUTOMACOES /
    "wp_mnt_atm_ams_pni"
)


for path in [PATH_AUTOMACOES, PATH_LEV_PNI]:

    if str(path) not in sys.path:

        sys.path.insert(0,str(path))

from wp_mnt_atm_ams_pni.main import main as amostra_pni



def flx_3():
    # data_corte é utilizado para processos de fechamento e reprocessamento de bases

    print(f"[{datetime.now()}] [INFO] [carregamento de bases de dados]")
    amostra_pni()




def preparar_input(arquivo, pasta_destino):

    pasta_destino = Path(pasta_destino)
    pasta_destino.mkdir(parents=True, exist_ok=True)

    destino = pasta_destino / arquivo.name

    with open(destino, "wb") as f:
        f.write(arquivo.getbuffer())

    return destino