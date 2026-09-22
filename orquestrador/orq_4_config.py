import streamlit as st
from pathlib import Path
from configparser import ConfigParser


PASTA_CONFIG = (
    Path.home()
    / "Documents"
    / "wp_central_atm"
    )

ARQUIVO_CONFIG = PASTA_CONFIG / "config.ini"

def carregar_config():
    """Carrega a configuração local do usuário."""

    if not ARQUIVO_CONFIG.exists():
        return ""

    config = ConfigParser()
    config.read(
        ARQUIVO_CONFIG,
        encoding="utf-8"
    )

    return config.get(
        "datalake",
        "caminho",
        fallback=""
    )


def salvar_config(caminho):
    """Salva o caminho do Data Lake."""

    PASTA_CONFIG.mkdir(
        parents=True,
        exist_ok=True
    )

    config = ConfigParser()

    config["datalake"] = {
        "caminho": caminho
    }

    with open(
        ARQUIVO_CONFIG,
        "w",
        encoding="utf-8"
    ) as arquivo:

        config.write(arquivo)