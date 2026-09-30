from configparser import ConfigParser
from pathlib import Path
# Regras e valores específicos do processo.
# Este é o principal arquivo para revisão dos hardcodes.

config = ConfigParser()

config.read(
        Path.home() / "Documents" / "wp_central_atm" / "config.ini",
        encoding="utf-8"
)

dl = Path.home() / config["datalake"]["caminho"]

datalake = str(dl)
# ABA DE CONFIGURAÇÃOC:\Users\luiz.farias\Numerator International\BKO - Documents\projeto-dados-ops\do_mf_usage\rbc

rbc_path = f'{datalake}/do_mf_usage/rbc'
input_projeto = f'{datalake}/do_mf_usage/input'
output_projeto = f'{datalake}/do_mf_usage/output'


COLUNAS_DESCARTAR = {
    "CdC06", "Clas06",
    "CdC07", "Clas07",
    "CdC08", "Clas08",
    "CdC09", "Clas09",
}

VALORES_AUSENTES = {
    "Clas01": ["NAO INFORMADO"],
    "Clas02": ["NAO INFORMADO"],
    "Clas03": ["NAO INFORMADO"],
    "Clas04": ["NAO INFORMADO"],
    "Clas05": ["NAO INFORMADO"],
    "Marca": ["NAO REQUERIDO", "NAO INFORMADO", "Sem Marca"],
    "Fabricante": ["NAO REQUERIDO", "NAO INFORMADO"],
    "Sub": ["Codebook VS"],
}

NORMALIZACOES_EXATAS = {
    "Agua Embalada": "Agua Mineral",
    "Snacks": "Salgadinho",
}

SUB_EXCLUIDOS = {
    "Codebook OOH",
    "Codebook OOH Barra / Tablete / Candy Bar",
    "Codebook OOH Batata Frita Na Hora",
    "Codebook OOH Bolos Industrializados",
    "Codebook OOH Bombom",
    "Codebook OOH Bombom Individual / Trufa",
    "Codebook OOH Caixa de Chocolate / Pacote de Choco",
    "Codebook OOH Casquinha",
    "Codebook OOH Chopeira",
    "Codebook OOH Com Gas",
    "Codebook OOH Copo / Pote",
    "Codebook OOH De Beber",
    "Codebook OOH De Colher",
    "Codebook OOH Doce",
    "Codebook OOH Docinhos e Tortas",
    "Codebook OOH Lata / Garrafa",
    "Codebook OOH Líquido",
    "Codebook OOH Nao Informado",
    "Codebook OOH Outros Formatos",
    "Codebook OOH Picolé",
    "Codebook OOH Pipoca Pronta",
    "Codebook OOH Salgadinhos Industrializados",
    "Codebook OOH Salgado",
    "Codebook OOH Salgados preparado na hora",
    "Codebook OOH Sem Gas",
    "Codebook OOH Suco de Frutas Feito na Hora",
    "Codebook OOH Suco de Frutas Industrializado",
}

ATIVOS_EXCLUIDOS = {"AR"}

# Regras específicas da classificação parcial do notebook original.
REGRAS_CLASSIFICACAO_PARCIAL = {
    200: "Clas01",
    63: "Clas02",
    686: "Sub",
    201: "Sub",
    58: "Sub",
    287: "Producto",
    212: "Sub",
    622: "Sub",
    269: "Clas02",
}

CORRECOES_CLASSIFICACAO = {
    "MISTA (VEGETAL + MANTEIGA)": "MARGARINA + MANTEIGA / MISTA",
    "DOCINHOS / RECHEIOS / COBERTOS": "LEITE CONDENSADO",
    "FIAMBRE / AFIAMBRADO / LANCHE": "FIAMBRE / AFIAMBRADO",
}

VALOR_NAO_CLASSIFICADO = "o"

RESULTADO_RBC = "Classificado Com RBC"
RESULTADO_HISTORICO = "Classificado Com Histórico"
RESULTADO_PARCIAL = "Classificação Parcial"
RESULTADO_CONFLITO = "Conflito"
RESULTADO_PARCIAL_RESOLVIDA = "Classificação Parcial Resolvida"
