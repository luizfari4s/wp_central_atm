# pages/pg_1_amostra_viva.py
import streamlit as st
import logging
import contextlib
from pathlib import Path
import sys
from urllib.parse import quote
from datetime import datetime
from os import getlogin

#from orquestrador.orq_1_rct_inhome import flx_1
# ROOT = PROD
ROOT = Path(__file__).resolve().parent
print(ROOT)


if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from orquestrador.orq_2_rct_inhome import flx_2
from orquestrador.orq_2_rct_inhome import preparar_input_ficha


st.title("Recrutados In Home | Top Client")

st.write(
    "Automação para fluxo de entrada e validação de qualidade de cadastro"
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

    arquivo_ficha = st.file_uploader(
        "📤 Selecione o arquivo da ficha",
        type=["xlsx", "xls", "csv"],
        accept_multiple_files=True
    )


    # =========================================================
    # EXECUÇÃO
    # =========================================================

    if st.button(
        "▶ Processar Recrutamento Top Client",
        use_container_width=True
    ):


        if arquivo_ficha is None:

            st.warning(
                "⚠️ Selecione a ficha antes de iniciar o processamento."
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
                    "🔄 Processando Recrutamento Top Client..."
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

                        for arquivo in arquivo_ficha:

                            preparar_input_ficha(
                                arquivo=arquivo
                            )


                        # =====================================
                        # ETAPA 2 - PROCESSAMENTO
                        # =====================================

                        flx_2(None)


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


with st.expander("📁 Ver histórico de processamentos",expanded=False):
    
    PASTA_HISTORICO = Path(f'C:/Users/{getlogin()}/Numerator International/BKO - Documents/projeto-dados-ops/do_ficha/tc/output_validacao')
    arquivos = list(PASTA_HISTORICO.glob("*.xlsx"))
    URL_BASE_SHAREPOINT = (
        "https://numeratorinternational.sharepoint.com"
        "/sites/BKO/Shared%20Documents"
        "/projeto-dados-ops/do_ficha/tc/output_validacao"
    )

    def montar_url_sharepoint(arquivo):

        nome_arquivo = quote(arquivo.name)

        return f"{URL_BASE_SHAREPOINT}/{nome_arquivo}"

    arquivos = sorted(
        PASTA_HISTORICO.glob("*.xlsx"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )


    for arquivo in arquivos[:5]:

        data_modificacao = datetime.fromtimestamp(
                arquivo.stat().st_mtime
            )

        url_arquivo = montar_url_sharepoint(arquivo)

        st.markdown(
                f"📄 [{arquivo.name}]({url_arquivo})"
            )

        st.caption(
                f"🕒 {data_modificacao.strftime('%d/%m/%Y %H:%M')}"
            )





















