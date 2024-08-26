import streamlit as st
import requests
import asyncio

@st.cache_data
def get_rate():
    cdi_sum = asyncio.run(get_cdi_rate())
    if cdi_sum is None:
        cdi_sum = 11.5  
    return cdi_sum

async def get_cdi_rate():
    try:
        response = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.4391/dados?formato=json")
        response.raise_for_status()  
        cdi_data = response.json()
        
        
        cdi_filtered = [float(entry['valor']) for entry in cdi_data[-14:-2]]  
        if cdi_filtered:
            cdi_sum = sum(cdi_filtered)
            return cdi_sum
    except requests.RequestException as e:
        st.error(f'Erro na requisição da API: {e}, usando valor padrão.')
    except ValueError as e:
        st.error(f'Erro ao processar a resposta da API: {e}, usando valor padrão.')
    return None

def calcular_cdi(taxa_cdi, valor_inicial, tempo, valor_contribuicao, unidade_tempo, multiplicar_cdi):
    taxa_cdi = taxa_cdi * multiplicar_cdi / 100
    
    if unidade_tempo == "Meses":
        anos = tempo / 12
    else:
        anos = tempo
    
    
    valor_anual = valor_inicial * (1 + taxa_cdi) ** anos
    

    valor_mensal = (1 + taxa_cdi) ** (1 / 12) - 1
    meses = int(anos * 12)
    
    valor_final_contribuicao = valor_contribuicao * (((1 + valor_mensal) ** meses - 1) / valor_mensal)
    
    
    valor_total = valor_anual + valor_final_contribuicao
    
    
    return valor_total

st.title('Simulador de Investimentos Cofrinhos')
st.write('Realize uma comparação entre a rentabilidade de diferentes bancos')

cdi_sum = get_rate()

st.markdown(f"<h6 style='text-align: center; margin: 20px;'>Taxa CDI {round(cdi_sum, 3)}%</h6>", unsafe_allow_html=True)

valor_inicial = st.number_input("Valor Inicial (R$)", min_value=0.0, step=100.0)
valor_contribuicao = st.number_input("Contribuição Mensal (R$)", min_value=0.0, step=100.0)
banco = st.selectbox("Selecione o Banco", ["Cofrinho Inter - 100% CDI", "Cofrinho Nubank  - 100% CDI", "Cofrinho PicPay - 102% CDI"])
unidade_tempo = st.selectbox("Unidade de Tempo", ["Anos", "Meses"])
tempo = st.number_input(f"Tempo de Investimento ({unidade_tempo})", min_value=1)

multiplicar_cdi = 1.02 if banco == "Cofrinho PicPay - 102% CDI" else 1.0

if st.button("Calcular"):
    resultado = calcular_cdi(cdi_sum, valor_inicial, tempo, valor_contribuicao, unidade_tempo, multiplicar_cdi)
    st.write(f"Retorno do Investimento: R$ {resultado:,.2f}")
