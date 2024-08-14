import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import requests
import asyncio
import datetime

@st.cache_data
def get_rates():
    cdi = asyncio.run(get_cdi_rate())
    selic = asyncio.run(get_selic_rate())
    tr = asyncio.run(get_tr_rate())
    if cdi == None:
        cdi = 11.5
    if selic == None:
        selic = 10.5
    if tr == None:
        tr = 0.0744
    return cdi, selic, tr

async def get_cdi_rate():
    try:
        response = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.4391/dados?formato=json")
        if response.ok:
            cdi_v = response.json()[-14:-2]
            cdi_v = sum([float(o['valor']) for o in cdi_v])
            return cdi_v
    except Exception as e:
        st.error("Erro ao obter a taxa CDI. Usando valor padrão.")

async def get_selic_rate():
    try:
        response = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados?formato=json")
        if response.ok:
            selic_v = response.json()[-13:-1]
            selic_v = sum([float(o['valor']) for o in selic_v])
            return selic_v
    except Exception as e:
        st.error("Erro ao obter a taxa Selic. Usando valor padrão.")

async def get_tr_rate():
    try:
        response = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.226/dados?formato=json")
        if response.ok:
            tr_v = float(response.json()[-1]['valor'])
            return tr_v
    except Exception as e:
        st.error("Erro ao obter a Taxa Referencial (TR). Usando valor padrão.")

def calculate_cdb(initial_value, cdb_rate, cdi_rate, years, contribution_value):
    cdi_rate /= 100
    cdb_rate /= 100
    final_rate = cdb_rate * cdi_rate
    final_value = initial_value * (1 + final_rate) ** years
    monthly_rate = (1 + final_rate) ** (1 / 12) - 1
    months = int(years * 12)
    final_contribution_value = contribution_value * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    total_value = final_value + final_contribution_value
    total_earnings = total_value - initial_value - (contribution_value * months)

    tax_rate = 0.15 
    if years <= 0.5:
        tax_rate = 0.225
    elif years <= 1:
        tax_rate = 0.20
    elif years <= 2:
        tax_rate = 0.175
    else:
        tax_rate = 0.15
    
    taxes = total_earnings * tax_rate
    return_value = total_value - taxes

    return return_value

def calculate_lci_lca_final_value(initial_value, lc_rate, cdi_rate, years, contribution_value):
    cdi_rate /= 100  
    lc_rate /= 100  
    months = int(years * 12)
    final_value = initial_value * (1 + lc_rate * cdi_rate) ** years
    monthly_rate = (1 + lc_rate * cdi_rate) ** (1 / 12) - 1
    future_value_contributions = contribution_value * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    return final_value + future_value_contributions

def calculate_savings(initial_value, selic_rate, years, contribution_value, ref_rate):
    if selic_rate <= 8.5:
        monthly_rate = 0.007
    else:
        monthly_rate = 0.005
    
    monthly_rate += (ref_rate / 100)
    
    months = int(years * 12)
    
    final_value = initial_value * (1 + monthly_rate) ** months
    future_value_contributions = contribution_value * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    return final_value + future_value_contributions

st.title("Simulador de Ativos de Renda Fixa")
st.write("Realize uma comparação entre a rentabilidade de diferentes tipos de investimentos em renda fixa! Ativos incluídos até o momento: CDB, LCI/LCA e Poupança")

state_vars = ['duration_unit', 'cdi', 'selic', 'tr']
if not all(key in st.session_state for key in state_vars):
    cdi, selic, tr = get_rates()
    st.session_state['duration_unit'] = 'Meses'
    st.session_state['cdi'] = cdi
    st.session_state['selic'] = selic
    st.session_state['tr'] = tr

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<h6 style='text-align: center; margin: 20px;'>CDI: {st.session_state['cdi']}</h6>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<h6 style='text-align: center; margin: 20px;'>Selic: {st.session_state['selic']}</h6>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<h6 style='text-align: center; margin: 20px;'>TR: {st.session_state['tr']}</h6>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col2:
    monthly_contribution = st.number_input("Aporte Mensal (R$)", step=100.0)
    st.session_state['duration_unit'] = st.selectbox("Unidade de Tempo", ["Meses", "Anos"])
    lci_lca_rentability = st.number_input("Rentabilidade da LCI/LCA (% do CDI)", value=85.0, min_value=0.0, max_value=300.0, step=10.0)
with col1:
    investment_value = st.number_input("Investimento Inicial (R$)", value=1000.0, min_value=0.0, step=100.0)
    duration_value = st.number_input(f"Vencimento ({st.session_state['duration_unit']})", value=1, min_value=1, step=1)
    cdb_rentability = st.number_input("Rentabilidade do CDB (% do CDI)", value=100.0, min_value=0.0, max_value=300.0, step=10.0)

if st.session_state['duration_unit'] == 'Meses':
    years = duration_value / 12
else:
    years = duration_value

if st.button("Simular Ativo", use_container_width=True):
    cdi = st.session_state['cdi']
    selic = st.session_state['selic']
    tr = st.session_state['tr']
    
    months = np.arange(0, int(years * 12) + 1, 1)
    
    cdb_growth = []
    lci_lca_growth = []
    savings_growth = []
    
    for month in months:
        month_years = month / 12
        cdb_value = calculate_cdb(investment_value, cdb_rentability, cdi, month_years, monthly_contribution)
        lci_lca_value = calculate_lci_lca_final_value(investment_value, lci_lca_rentability, cdi, month_years, monthly_contribution)
        savings_value = calculate_savings(investment_value, selic, month_years, monthly_contribution, tr)
        
        cdb_growth.append(cdb_value)
        lci_lca_growth.append(lci_lca_value)
        savings_growth.append(savings_value)
    
    start_date = datetime.datetime.now()
    date_range = pd.date_range(start=start_date, periods=len(months), freq='M')
    month_names = date_range.strftime('%B %Y')

    df = pd.DataFrame({
        'Mês': month_names,
        'CDB': cdb_growth,
        'LCI/LCA': lci_lca_growth,
        'Poupança': savings_growth
    })
    
    fig = px.line(df, x='Mês', y=['CDB', 'LCI/LCA', 'Poupança'], 
                  title='Comparação de Crescimento de Investimentos ao Longo do Tempo',
                  labels={'value': 'Valor Acumulado (R$)', 'Mês': 'Tempo'},
                  markers=True, template="plotly_dark")

    fig.update_layout(
        xaxis_title='Tempo',
        yaxis_title='Valor Acumulado (R$)',
        legend_title='Investimentos',
        font=dict(size=12),
        autosize=False,
        width=900,
        height=500
    )

    fig.update_traces(line=dict(width=4))

    st.plotly_chart(fig, use_container_width=True)
