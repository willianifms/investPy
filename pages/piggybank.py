import streamlit as st
import plotly.express as px
import pandas as pd 
import numpy as np 
import requests 
import asyncio
import datetime 
 


@st.cache_data
def get_rate():
    cdi = asyncio.run(get_cdi_rate())
    if cdi is None:
        cdi = 11.5
    return cdi

async def get_cdi_rate():
    try:
        response = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.4391/dados?formato=json")
        if response.ok:
            cdi_v = response.json()[-14:-2]
            cdi_v = sum([float(o['valor']) for o in cdi_v])
            return cdi_v
    except Exception as e:
        st.error('Erro ao obter a taxa do CDI, usando valor padrão.')


def calcular_cdi(taxa_cdi, valor_inicial, tempo, valor_contribuicao, unidade_tempo):
    taxa_cdi /= 100
    
    if unidade_tempo == "Meses":
        anos = tempo / 12
    else:
        anos = tempo
    
    valor_anual = valor_inicial * (1 + taxa_cdi) ** anos
    
    valor_mensal = (1 + taxa_cdi) ** (1 / 12) - 1
    meses = int(anos * 12)
    
    valor_final_contribuicao = valor_contribuicao * (((1 + valor_mensal) ** meses - 1) / valor_mensal)
    
    valor_total = valor_anual + valor_final_contribuicao
    
    ganhos_totais = valor_total - valor_inicial - (valor_contribuicao * meses)
    
    taxa_de_imposto = 0.15
    if anos <= 0.5:
        taxa_de_imposto = 0.225
    elif anos <= 1:
        taxa_de_imposto = 0.20
    elif anos <= 2:
        taxa_de_imposto = 0.175
    else:
        taxa_de_imposto = 0.15 
    
    impostos = ganhos_totais * taxa_de_imposto 
    valor_retorno = valor_total - impostos
    return valor_retorno


st.title('Simulador de Investimentos em Cofrinhos')
st.write('Realize uma comparação entre a rentabilidade de diferentes bancos')


cdi = get_rate()


st.markdown(f"<h6 style='text-align: center; margin: 20px;'>CDI: {round(cdi, 3)}%</h6>", unsafe_allow_html=True)


valor_inicial = st.number_input("Valor Inicial (R$)", min_value=0.0, step=100.0)

valor_contribuicao = st.number_input("Contribuição Mensal (R$)", min_value=0.0, step=100.0)

banco = st.selectbox("Selecione o Banco", ["Cofrinho Inter - 100% CDI", "Cofrinho Nubank  - 100% CDI", "Cofrinho PicPay - 102% CDI"])

unidade_tempo = st.selectbox("Unidade de Tempo", ["Anos", "Meses"])

tempo = st.number_input(f"Tempo de Investimento ({unidade_tempo})", min_value=1)

if banco == "Cofrinho PicPay - 102% CDI":
    multiplicar_cdi = 1.02
else:
    multiplicar_cdi = 1.0


if st.button("Calcular"):
    resultado = calcular_cdi(cdi, valor_inicial, tempo, valor_contribuicao, unidade_tempo,multiplicar_cdi)
    st.write(f"Retorno do Investimento: R$ {resultado:,.2f}")
