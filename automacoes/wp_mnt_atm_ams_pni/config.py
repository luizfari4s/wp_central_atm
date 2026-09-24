# Regras e caminhos mantidos conforme o notebook original.
from configparser import ConfigParser
from pathlib import Path

config = ConfigParser()

config.read(
        Path.home() / "Documents" / "wp_central_atm" / "config.ini",
        encoding="utf-8"
)

dl = Path.home() / config["datalake"]["caminho"]

datalake = str(dl)
# ABA DE CONFIGURAÇÃO

input_projeto = f'{datalake}/do_ams_pni/input'
output_projeto = f'{datalake}/do_ams_pni/output'
nrperfil = f'{datalake}/do_bases/TopClient'
gac = f'{datalake}/do_gacode'

# Regras hard-coded do notebook
ORIGENS_PNI = [1, 2, 3, 4, 18, 16]
ORIGENS_EXP = [20, 21, 22, 23]

BINS_CANDIDATOS = [-1, 0, 1, 3, 6, float('inf')]
LABELS_CANDIDATOS = [
    '0 candidatos', '1 candidato', '2-3 candidatos',
    '4-6 candidatos', '7+ candidatos'
]
ORDEM_CANDIDATOS = [
    '0 candidatos', '1 candidato', '2-3 candidatos',
    '4-6 candidatos', '7+ candidatos'
]
