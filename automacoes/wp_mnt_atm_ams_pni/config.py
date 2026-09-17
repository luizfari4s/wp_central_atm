# Regras e caminhos mantidos conforme o notebook original.
from os import getlogin

dominio_interno = getlogin()
input_projeto = f'/do_ams_pni/input'
output_projeto = f'/do_ams_pni/output'
nrperfil = f'/do_bases/TopClient/'
datalake = f'C:/Users/{dominio_interno}/Numerator International/BKO - Documents/projeto-dados-ops'
gac = '/do_gacode'

# Regras hard-coded do notebook
# Revisar se origem PNI na verdade não é PNC
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
