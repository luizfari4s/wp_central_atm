import streamlit as st


# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(
    page_title="ATMCENTRAL",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CSS - APARÊNCIA DA CENTRAL
# =========================================================

st.markdown("""
<style>

/* Remove elementos desnecessários */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* Espaçamento principal */

.block-container {
    max-width: 1100px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}


/* Título */

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 0px;
}


/* Subtítulo */

.subtitle {
    font-size: 18px;
    opacity: 0.7;
    margin-top: 0px;
    margin-bottom: 35px;
}


/* Cabeçalho das equipes */

.stExpander {

    border-radius: 10px;

}


/* Botões */

.stButton > button {

    width: 100%;
    text-align: left;

    border-radius: 8px;

    padding: 12px 18px;

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# CABEÇALHO
# =========================================================

st.markdown(
    """
    <div class="main-title">
        ⚙️ ATMCENTRAL
    </div>

    <div class="subtitle">
        Central de Automações e Processos
    </div>
    """,
    unsafe_allow_html=True
)


st.divider()


# =========================================================
# TEXTO INICIAL
# =========================================================

st.subheader("Automações disponíveis")

st.write(
    "Selecione uma equipe para visualizar as automações disponíveis."
)

st.write("")


# =========================================================
# EQUIPE OOH
# =========================================================

with st.expander("Out Off Home", expanded=False):


    # -----------------------------------------------------
    # AMOSTRA VIVA
    # -----------------------------------------------------

    col1, col2 = st.columns([4, 1])

    with col1:

        st.markdown("""
        **Amostra Viva**

        Atualização e processamento da base de Amostra Viva.
        """)

    with col2:

        if st.button(
            "Acessar",
            key="btn_amostra_viva",
            use_container_width=True
        ):

            st.switch_page(
                "pages/pg_1_amostra_viva.py"
            )


    st.divider()


    # -----------------------------------------------------
    # CHURN
    # -----------------------------------------------------

    col1, col2 = st.columns([4, 1])

    with col1:

        st.markdown("""
        **Churn (em implantação)**

        Processamento e análise dos dados de Churn.
        """)

    with col2:

        if st.button(
            "Acessar",
            key="btn_churn",
            use_container_width=True
        ):

            st.switch_page(
                "pages/02_churn.py"
            )


    st.divider()


    # -----------------------------------------------------
    # PONTUAÇÃO DO PAINEL
    # -----------------------------------------------------

    col1, col2 = st.columns([4, 1])

    with col1:

        st.markdown("""
        **Pontuação do Painel (em implantação)**

        Processamento das regras de pontuação do painel.
        """)

    with col2:

        if st.button(
            "Acessar",
            key="btn_pontuacao",
            use_container_width=True
        ):

            st.switch_page(
                "pages/03_pontuacao_painel.py"
            )


# =========================================================
# OUTRAS EQUIPES
# =========================================================

            
with st.expander("Qualidade Amostral"):

    col1, col2 = st.columns([4, 1])

    with col1:
    
        st.markdown("""
        **Validação de fichas InHome**
    
        Validação de qualidade de cadastro dos recrutados Top Client
        """)
    with col2:
    
        if st.button(
            "Acessar",
            key="btn_rtc_inhome",
            use_container_width=True
        ):
    
            st.switch_page(
                    "pages/pg_2_rct_inhome.py"
            )
    st.divider()

    col1, col2 = st.columns([4, 1])
            
    with col1:
            
            st.markdown("""
            **Levantamento de Amostra PNI**
            
            Determinação de amostra para o painel PNI
            """)
    with col2:
            
        if st.button(
            "Acessar",
            key="btn_lev_pni",
            use_container_width=True
        ):
            
            st.switch_page(
                    "pages/pg_3_lev_pni.py"
            )

    st.divider()


    col1, col2 = st.columns([4, 1])

    
    with col1:
        
            st.markdown("""
            **Levantamento Sample Balance (em implandação)**
        
            Revisão do acompanhamento de sample balance e dados PNC
            """)
    with col2:
        
            if st.button(
                "Acessar",
                key="btn_lv_balance",
                use_container_width=True
            ):
        
                st.switch_page(
                        "pages/pg_2_rct_inhome.py"
                )
    

with st.expander("Usage"):

    col1, col2 = st.columns([4, 1])

    with col1:
    
        st.markdown("""
        **Masterfile Usage (Em Implantação)**
    
        Construção de base e classificações de produtos para USAGE
        """)
    with col2:
    
        if st.button(
            "Acessar",
            key="btn_mf_usage_br",
            use_container_width=True
        ):
    
            st.switch_page(
                    "pages/pg_2_rct_inhome.py"
            )
    st.divider()

    col1, col2 = st.columns([4, 1])
            
    with col1:
            
            st.markdown("""
            **Validação de coleta Usage (Em Implantação)**
            
            Analise, treinamento e validação de pratos declarados no usage
            """)
    with col2:
            
        if st.button(
            "Acessar",
            key="btn_vl_prataos",
            use_container_width=True
        ):
            
            st.switch_page(
                    "pages/pg_3_lev_pni.py"
            )
    

st.subheader("Processos Gerais")

st.write(
    "Selecione o fluxo para visualizar"
)

st.write("")



with st.expander('Dados Gerenciais'):

    st.divider()
         
         
    col1, col2 = st.columns([4, 1])
         
             
    with col1:
                 
                     st.markdown("""
                     **Levantamento Amostra Geral manutenção (em implandação)**
                 
                     Atualização e manutenção da amostra geral
                     """)
    with col2:
                 
                     if st.button(
                         "Acessar",
                         key="btn_ams_mnt",
                         use_container_width=True
                     ):
                 
                         st.switch_page(
                                 "pages/pg_2_rct_inhome.py"
                         )

    st.divider()
         
         
    col1, col2 = st.columns([4, 1])
         
             
    with col1:
                 
                     st.markdown("""
                     **Levantamento Amostra Geral Recrutamento (em implandação)**
                 
                     Atualização e manutenção da amostra geral
                     """)
    with col2:
                 
                     if st.button(
                         "Acessar",
                         key="btn_ams_rct",
                         use_container_width=True
                     ):
                 
                         st.switch_page(
                                 "pages/pg_2_rct_inhome.py"
                         )

    st.divider()
             
             
    col1, col2 = st.columns([4, 1])
             
                 
    with col1:
                     
                         st.markdown("""
                         **Configuração geral**
                     
                         Ajustar caminhos relativos à pastas
                         """)
    with col2:
                     
                if st.button(
                    "Acessar",
                    key="btn_config",
                    use_container_width=True
                    ):
                     
                    st.switch_page(
                     "pages/pg_4_config.py"
                             )




st.divider()

st.caption(
    "ATMCENTRAL • Central de Automações e Processos"
)
