import streamlit as st

st.title('📈 InvestData')
st.write("O InvestData é um aplicativo que te ajuda a planejar seus investimentos de forma simples e intuitiva. Com ele, você pode:")
st.markdown("* Simular diferentes cenários de investimento em renda fixa")
st.markdown("* Comparar a rentabilidade de diversos tipos de ativos")
st.markdown("* Aprender sobre o universo dos investimentos")
st.header("Comece agora mesmo!")

# Botões para navegar para as outras páginas
st.page_link("./pages/custom.py", label="Simular Ativo Personalizado", icon="💰")
st.page_link("./pages/piggybank.py", label="Simular Cofrinhos Populares", icon="🐷")
