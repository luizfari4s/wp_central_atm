from pathlib import Path
import sys
from datetime import datetime

from pathlib import Path
import sys

# =====================================================
# CAMINHO DA AUTOMAÇÃO
# =====================================================

ROOT = Path(__file__).resolve().parent.parent

PATH_AUTOMACAO = (
    ROOT
    / "automacoes"
    / "wp_ooh_atm_amostra_viva_ooh"
)


if str(PATH_AUTOMACAO) not in sys.path:
    sys.path.insert(0, str(PATH_AUTOMACAO))


# =====================================================
# IMPORT DA AUTOMAÇÃO
# =====================================================

from automacoes.wp_ooh_atm_amostra_viva_ooh.main_nr import (
    main as atualizar_amostra_viva
)

from automacoes.wp_ooh_atm_amostra_viva_ooh.functions import (
    logger
)

def flx_1(mes_atual,d=0):
    # Fluxo 1: Aqui devemos automatizar apenas a execução normal, mediante o recebimento de parametros
    
    atualizar_amostra_viva(
        type='rt',
        inicio=mes_atual,
        fim='',
        day_minus=d-1
        
    )


