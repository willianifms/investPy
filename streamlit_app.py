import streamlit as st

# Definição das páginas
home_page = st.Page("./pages/home.py", title="O que é o InvestData?", icon="🏠")
custom_page = st.Page("./pages/custom.py", title="Renda Fixa", icon="💰")
piggybank_page = st.Page("./pages/piggybank.py", title="Cofrinhos", icon="🐷")

# Configuração da navegação entre páginas
pg = st.navigation({
    "Bem-vindo (a)": [home_page],
    "Simuladores": [custom_page, piggybank_page]
})

pg.run()