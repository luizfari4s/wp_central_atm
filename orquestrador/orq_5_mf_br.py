import streamlit as st
from pathlib import Path
from configparser import ConfigParser
from pathlib import Path
import sys
# Regras e valores específicos do processo.
# Este é o principal arquivo para revisão dos hardcodes.

config = ConfigParser()

config.read(Path.home() / "Documents" / "wp_central_atm" / "config.ini", encoding="utf-8")

dl = Path.home() / config["datalake"]["caminho"]

datalake = str(dl)
# ABA DE CONFIGURAÇÃOC:\Users\luiz.farias\Numerator International\BKO - Documents\projeto-dados-ops\do_mf_usage\rbc

rbc_path = f'{datalake}/do_mf_usage/rbc'
input_projeto = f'{datalake}/do_mf_usage/input'
output_projeto = f'{datalake}/do_mf_usage/output'
# Raiz do projeto wp_central_atm
ROOT = Path(__file__).resolve().parent.parent

PATH_AUTOMACOES = ROOT / "automacoes"

PATH = (PATH_AUTOMACOES / "wp_usage_atm_masterfile")


for path in [PATH_AUTOMACOES, PATH]:

    if str(path) not in sys.path:

        sys.path.insert(0,str(path))

from wp_usage_atm_masterfile.main import main as mf_br


def flx_5():

    mf_br(
        rule_table_path=str(rbc_path) + "/rule_table_with_rulemap_v2.csv",
                level_data_path=str(rbc_path) + "/level_data.CSV",
                rbc_paths={
                    "N1": str(rbc_path) + "/RBC_N1.CSV",
                    "N2": str(rbc_path) + "/RBC_N2.CSV",
                    "N3": str(rbc_path) + "/RBC_N3.CSV",
                    "N4": str(rbc_path) + "/RBC_N4.CSV"},
        masterfile_path=str(input_projeto) + "/MF_Atual.CSV",
        caminho_saida=str(output_projeto) + "/MF_BR_USAGE_teste.csv",
    )


def preparar_input(arquivo, pasta_destino):

    pasta_destino = Path(pasta_destino)
    pasta_destino.mkdir(parents=True, exist_ok=True)

    destino = pasta_destino / arquivo.name

    with open(destino, "wb") as f:
        f.write(arquivo.getbuffer())

    return destino