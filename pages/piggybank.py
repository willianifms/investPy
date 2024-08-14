import streamlit as st

def calcular_valor_final(investimento_inicial, taxa_de_juros, anos):
    return investimento_inicial * (1 + taxa_de_juros) ** anos


st.title("Simulador de Investimentos")
investimento_inicial = st.number_input('Digite o valor inicial do investimento:', min_value=0.0, step=100.0)
anos = st.number_input('Quantos anos será o tipo de investimento?', min_value=1, step=1)


tipo_investimento = st.selectbox('Qual será o tipo de investimento?', 
                                 ['Cofrinho do Inter (Rende 100% do CDI)', 
                                  'Cofrinho do Nubank (Rende 100% do CDI)', 
                                  'Cofrinho do PicPay (Rende 102% do CDI)'])


if tipo_investimento == 'Cofrinho do Inter (Rende 100% do CDI)':
    taxa_de_juros = 0.104
elif tipo_investimento == 'Cofrinho do Nubank (Rende 100% do CDI)':
    taxa_de_juros = 0.104
elif tipo_investimento == 'Cofrinho do PicPay (Rende 102% do CDI)':
    taxa_de_juros = 0.1061
else:
    st.error('Escolha uma opção válida!')
    taxa_de_juros = 0
 
if st.button("Calcular"):
    valor_final = calcular_valor_final(investimento_inicial, taxa_de_juros, anos)
    st.success(f"O valor final após {anos} anos será de: R$ {valor_final:.2f}")
