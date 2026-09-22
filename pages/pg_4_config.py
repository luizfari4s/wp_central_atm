# pages/01_amostra_viva.py
import streamlit as st
import contextlib
from pathlib import Path
import sys
from urllib.parse import quote
from datetime import date, timedelta,datetime
from os import getlogin
from orquestrador.orq_4_config import salvar_config,carregar_config
    # ============================================================
# PÁGINA
# ============================================================

st.title("⚙️ Configuração")

st.subheader("Acesso ao Data Lake")

st.write(
    "Informe o caminho relativo do Data Lake "
    "a partir da sua pasta de usuário."
)
with st.expander("Parametros", expanded=False):
    caminho_atual = carregar_config()

    caminho = st.text_input(
        "Caminho relativo do Data Lake",
        value=caminho_atual,
        placeholder=(
            r"Numerator International\BKO - projeto-dados-ops"
        )
    )


    if st.button("💾 Salvar configuração"):

        caminho = caminho.strip()

        if not caminho:

            st.warning(
                "⚠️ Informe o caminho do Data Lake."
            )

        else:

            salvar_config(caminho)

            # Monta o caminho completo apenas para validar
            datalake = Path.home() / caminho

            if datalake.exists():

                st.success(
                    "✅ Configuração salva e Data Lake encontrado."
                )

                st.code(str(datalake))

            else:

                st.warning(
                    "⚠️ Configuração salva, "
                    "mas o caminho informado não foi encontrado."
                )

                st.code(str(datalake))