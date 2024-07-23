import streamlit as st

# `st.title(" My new app")` is a Streamlit function that sets the title of the web application to "My
# new app". This function is used to display a title at the top of the web page to provide a heading
# or a name for the application.
st.title("📈 InvestPy")
st.write(
    "Simulador de Investimentos"
)

    



option = st.selectbox(
    "Qual Será o tipo de investimento?",
    ("🏛 Cofrinho do Inter", "🏛 Cofrinho do Nubank", "🏛 Cofrinho do PicPay"))

st.write("Investimento selecionado:", option)

genre = st.radio(
    "Aporte inicial",
    ["Sim", "Não"],
    index=None,
)

if genre == "Sim":
    st.write("Digite o valor do aporte inicial")
    aporte = st.number_input('Valor do aporte', value=0)
    st.write("Aporte inicial:", aporte)
    
mensal = st.radio(
    "Investimento Mensal",
    ["Sim", "Não"],
    index=None,
)

if mensal == "Sim":
    st.write("Digite o valor do aporte mensal")
    aporte_mensal = st.number_input('Valor do aporte mensal')
    st.write("Aporte mensal:", aporte_mensal)


tempoInvestimento = st.selectbox(
    "Qual Será o tipo de investimento?",
    ("1 ano", "3 anos", "5 anos", "10 anos", "20 anos", "30 anos"))

st.write("Investimento selecionado:", tempoInvestimento)

if option == "🏛 Cofrinho do Inter" and aporte_mensal >=1 or aporte >=1:
    st.title("📈 Resultado do investimento")
    resultAporte = aporte + (aporte ** 0.081)
    resultMensal = aporte_mensal + (aporte_mensal ** 0.081)
    result = resultAporte + resultMensal
    st.write("Aporte mensal:", result)