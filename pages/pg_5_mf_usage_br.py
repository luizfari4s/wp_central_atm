# pages/01_amostra_viva.py
# pages/pg_1_amostra_viva.py
import streamlit as st
import logging
import contextlib
from pathlib import Path
import sys
from urllib.parse import quote
from datetime import datetime
from os import getlogin
from orquestrador.orq_5_mf_br import flx_5,input_projeto
from orquestrador.orq_3_lev_pni import preparar_input

st.title("Geração e importação | PNI")

st.write(
    "Automação para seleção de individuos para participação do PNI"
)

with st.expander("Parametros", expanded=False):

    # =========================================================
    # CAPTURA DE STDOUT / PRINT
    # =========================================================

    class StreamlitOutput:

        def __init__(self, container, limite=10):

            self.container = container
            self.linhas = []
            self.limite = limite


        def write(self, mensagem):

            mensagem = mensagem.strip()

            if mensagem:

                self.linhas.append(mensagem)

                # Mantém apenas os últimos logs
                self.linhas = self.linhas[-self.limite:]

                self.container.code(
                    "\n".join(self.linhas),
                    language=None
                )


        def flush(self):

            pass


    # =========================================================
    # CAPTURA DO LOGGER
    # =========================================================

    class StreamlitLogHandler(logging.Handler):

        def __init__(self, output):

            super().__init__()

            self.output = output


        def emit(self, record):

            try:

                mensagem = self.format(record)

                self.output.write(mensagem)

            except Exception:

                self.handleError(record)


    # =========================================================
    # INPUT
    # =========================================================

    mf_atual = st.file_uploader(
        "Faça o upload do masterfile atualizado em CSV",
        type=["xlsx", "xls", "csv"]
    )

    # =========================================================
    # EXECUÇÃO
    # =========================================================

    if st.button(
        "▶ Processae Amostra PNI",
        use_container_width=True
    ):


        if ((mf_atual))is None:

            st.warning(
                "Selecione os dados antes de iniciar o processamento."
            )

        else:

            # =====================================
            # CONTAINER DOS LOGS
            # =====================================

            log_box = st.empty()


            # =====================================
            # CAPTURADOR ÚNICO
            # =====================================

            output = StreamlitOutput(
                container=log_box,
                limite=1
            )


            # =====================================
            # HANDLER DO LOGGER
            # =====================================

            streamlit_handler = StreamlitLogHandler(
                output=output
            )


            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
            )


            streamlit_handler.setFormatter(
                formatter
            )


            root_logger = logging.getLogger()


            try:

                # =====================================
                # CONFIGURA LOGGER
                # =====================================

                root_logger.setLevel(
                    logging.INFO
                )


                root_logger.addHandler(
                    streamlit_handler
                )


                with st.spinner(
                    "Processando Amostra PNI..."
                ):


                    # =====================================
                    # CAPTURA PRINTS
                    # =====================================

                    with contextlib.redirect_stdout(
                        output
                    ):


                        # =====================================
                        # ETAPA 1 - PREPARAR INPUT
                        # =====================================

                        preparar_input(
                            arquivo=mf_atual,
                            pasta_destino=f'{input_projeto}'
                        )

                        # =====================================
                        # ETAPA 3 - PROCESSAMENTO
                        # =====================================

                        flx_5()


                st.success(
                    "✅ Processamento concluído!"
                )


            except Exception as erro:

                st.error(
                    "❌ Erro durante o processamento."
                )

                st.exception(erro)


            finally:

                # =====================================
                # REMOVE HANDLER
                # =====================================

                if streamlit_handler in root_logger.handlers:

                    root_logger.removeHandler(
                        streamlit_handler
                    )

st.subheader("📁 Processamentos disponíveis")