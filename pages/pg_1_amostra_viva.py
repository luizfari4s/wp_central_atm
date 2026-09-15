# pages/01_amostra_viva.py
import streamlit as st
import contextlib
from pathlib import Path
import sys
from urllib.parse import quote
from datetime import date, timedelta,datetime
from os import getlogin
from orquestrador.orq_1_ooh import flx_1
# ROOT = PROD
ROOT = Path(__file__).resolve().parent
print(ROOT)


if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


st.title("📊 Amostra Viva")

st.write(
    "Automação para processamento da Amostra Viva."
)

# =========================================================
# LOG STREAMLIT
# =========================================================



with st.expander("Parametros", expanded=False):

    class StreamlitOutput:

        def __init__(self, container, limite=10):

            self.container = container
            self.linhas = []
            self.limite = limite


        def write(self, mensagem):

            if mensagem.strip():

                self.linhas.append(
                    mensagem.strip()
                )

                # Mantém apenas os últimos logs
                self.linhas = self.linhas[-self.limite:]

                self.container.code(
                    "\n".join(self.linhas),
                    language=None
                )


        def flush(self):

            pass


    # =========================================================
    # PARÂMETROS
    # =========================================================

    data_inicio = st.date_input(
        "📅 Data inicial do processamento",
        value=date.today().replace(day=1)
    )


    data_final_processamento = st.date_input(
        "📅 Data final do processamento",
        value=date.today()
    )


    # Calcula automaticamente quantos dias atrás
    day_minus = (
        date.today() - data_final_processamento
    ).days




    # =========================================================
    # EXECUÇÃO
    # =========================================================

    if st.button(
        "▶ Processar Amostra Viva",
        use_container_width=True
    ):

        # Container fixo para os logs
        log_box = st.empty()


        # Capturador do terminal
        output = StreamlitOutput(
            container=log_box,
            limite=1
        )


        try:

            with st.spinner(
                "🔄 Processando Amostra Viva..."
            ):

                with contextlib.redirect_stdout(output):

                    flx_1(
                        mes_atual=data_inicio.strftime("%d.%m.%Y"),
                        d=day_minus + 1
                    )


            st.success(
                "✅ Processamento concluído!"
            )


        except Exception as erro:

            st.error(
                "❌ Erro durante o processamento."
            )

            st.exception(erro)


st.subheader("📁 Processamentos disponíveis")


with st.expander("📁 Ver histórico de processamentos",expanded=False):
    
    sharepoint_path = f'C:/Users/luiz.farias/Numerator International/BKO - Documents/Report/Elegibilidade OOH/projeto_ooh/datalake/historico_eelegibilidade'
    PASTA_HISTORICO = Path(f'C:/Users/{getlogin()}/Numerator International/BKO - Documents/Report/Elegibilidade OOH/projeto_ooh/datalake/historico_eelegibilidade')
    arquivos = list(PASTA_HISTORICO.glob("*.xlsx"))

    URL_BASE_SHAREPOINT = (
        "https://numeratorinternational.sharepoint.com"
        "/sites/BKO/Shared%20Documents"
        "/Report/Elegibilidade%20OOH/projeto_ooh"
        "/datalake/historico_eelegibilidade"
    )

    def montar_url_sharepoint(arquivo):

        nome_arquivo = quote(arquivo.name)

        return f"{URL_BASE_SHAREPOINT}/{nome_arquivo}"

    arquivos = sorted(
        PASTA_HISTORICO.glob("*.xlsx"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )


    for arquivo in arquivos[:10]:

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






