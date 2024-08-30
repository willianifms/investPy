import streamlit as st
import plotly.express as px
import pandas as pd
import requests
import asyncio
import datetime

# Função para realizar a chamada das APIs do Banco Central e obter as taxas: CDI, SELIC e TAXA REFERENCIAL
@st.cache_data
def get_rates():
    cdi = asyncio.run(get_cdi_rate())
    selic = asyncio.run(get_selic_rate())
    tr = asyncio.run(get_tr_rate())
    if cdi is None:
        cdi = 11.5
    if selic is None:
        selic = 10.5
    if tr is None:
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

# Cálculo do CDB
def calculate_cdb(initial_value, cdb_rate, cdi_rate, years, contribution_value):
    # Conversão de % para decimal
    cdi_rate /= 100
    cdb_rate /= 100

    # Valor futuro do investimento inicial (juros compostos) i,t = anual
    # Fórmula dos Juros Compostos vista em sala
    # M = C * (1 + i)^t
    # final = inicial * (1 + taxa) ** years
    final_rate = cdb_rate * cdi_rate
    final_value = initial_value * (1 + final_rate) ** years

    # Valor futuro dos aportes mensais (valor futuro de anuidade ordinária) i,t = mensal
    # VF = C * (((1 + i)^t-1) / i)
    # monthly_rate = (1 + final_rate) ** (1/12) = i
    # months = int(years * 12) = t
    monthly_rate = (1 + final_rate) ** (1 / 12) - 1
    months = int(years * 12)
    final_contribution_value = contribution_value * (((1 + monthly_rate) ** months - 1) / monthly_rate)

    # Soma do rendimento dos montantes + rendimento do investimento inicial
    total_value = final_value + final_contribution_value
    
    # Extrair lucros totais para cálculo do IR :(
    total_earnings = total_value - initial_value - (contribution_value * months)

    # Cálculo do imposto a depender do tempo de aplicação
    tax_rate = 0.15 
    if years <= 0.5:
        tax_rate = 0.225
    elif years <= 1:
        tax_rate = 0.20
    elif years <= 2:
        tax_rate = 0.175
    else:
        tax_rate = 0.15
    
    # Aplicação do IR
    taxes = total_earnings * tax_rate
    return_value = total_value - taxes
    return return_value

# Cálculo do LCI/LCA
def calculate_lci_lca(initial_value, lc_rate, cdi_rate, years, contribution_value):
    # Conversão de % para decimal e de anos para meses
    cdi_rate /= 100  
    lc_rate /= 100  
    months = int(years * 12)

    # Valor futuro do investimento inicial
    # Fórmula dos Juros Compostos vista em sala
    # M = C * (1 + i)^t
    final_rate = lc_rate * cdi_rate
    final_value = initial_value * (1 + final_rate) ** years

    # Valor futuro dos aportes mensais (valor futuro de anuidade ordinária) i,t = mensal
    # VF = C * (((1 + i)^t-1) / i)
    # monthly_rate = (1 + final_rate) ** (1/12) = i
    # months = int(years * 12) = t
    monthly_rate = (1 + final_rate) ** (1 / 12) - 1
    future_value_contributions = contribution_value * (((1 + monthly_rate) ** months - 1) / monthly_rate)

    # Retorno do valor total, isento de IR :)
    return final_value + future_value_contributions

# Cálculo do rendimento da poupança
def calculate_savings(initial_value, selic_rate, years, contribution_value, ref_rate):
    # Calcular rentabilidade da poupança
    if selic_rate <= 8.5:
        monthly_rate = 0.007
    else:
        monthly_rate = 0.005
    
    monthly_rate += (ref_rate / 100)
    
    # Anos para meses
    months = int(years * 12)
    
    # Montante final
    # Novamente juros compostos
    final_value = initial_value * (1 + monthly_rate) ** months
    future_value_contributions = contribution_value * (((1 + monthly_rate) ** months - 1) / monthly_rate)

    # Retorno do valor total, também isento de IR :)
    return final_value + future_value_contributions

# Cabeçalho da página
st.title("Simulador de Ativos de Renda Fixa")
st.write("Realize uma comparação entre a rentabilidade de diferentes tipos de investimentos em renda fixa! Ativos incluídos até o momento: CDB, LCI/LCA e Poupança")

# Inicialização do estado da página
state_vars = ['duration_unit', 'cdi', 'selic', 'tr']
if not all(key in st.session_state for key in state_vars):
    cdi, selic, tr = get_rates()
    st.session_state['duration_unit'] = 'Meses'
    st.session_state['cdi'] = cdi
    st.session_state['selic'] = selic
    st.session_state['tr'] = tr

# Mostrar valores das taxas que estão sendo consideradas para o usuário
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<h6 style='text-align: center; margin: 20px;'>CDI: {round(st.session_state['cdi'], 3)}%</h6>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<h6 style='text-align: center; margin: 20px;'>Selic: {round(st.session_state['selic'], 3)}%</h6>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<h6 style='text-align: center; margin: 20px;'>TR: {round(st.session_state['tr'], 3)}%</h6>", unsafe_allow_html=True)

# Inputs do usuário
col1, col2 = st.columns(2)
with col2:
    monthly_contribution = st.number_input("Aporte Mensal (R$)", step=100.0)
    st.session_state['duration_unit'] = st.selectbox("Unidade de Tempo", ["Meses", "Anos"])
    lci_lca_rentability = st.number_input("Rentabilidade da LCI/LCA (% do CDI)", value=85.0, min_value=0.0, max_value=300.0, step=10.0)
with col1:
    investment_value = st.number_input("Investimento Inicial (R$)", value=1000.0, min_value=0.0, step=100.0)
    duration_value = st.number_input(f"Vencimento ({st.session_state['duration_unit']})", value=6, min_value=1, step=1)
    cdb_rentability = st.number_input("Rentabilidade do CDB (% do CDI)", value=100.0, min_value=0.0, max_value=300.0, step=10.0)

# Considerar unidade selecionada no selectbox
if st.session_state['duration_unit'] == 'Meses':
    years = duration_value / 12
else:
    years = duration_value

# Botão de simulação
if st.button("Simular Ativos", use_container_width=True):
    # Recuperar valores atuais das taxas relevantes
    cdi = st.session_state['cdi']
    selic = st.session_state['selic']
    tr = st.session_state['tr']
    
    # Estabelecendo intervalo de meses num array [0, 1, 2, ..., n]
    months = range(int(years * 12) + 1)
    
    # Inicializando array para obter o valor de crescimento mensal de cada investimento
    cdb_growth = []
    lci_lca_growth = []
    savings_growth = []
    
    # Calcular valor para cada um dos meses, a fim de exibir no gráfico
    for month in months:
        month_years = month / 12
        cdb_value = calculate_cdb(investment_value, cdb_rentability, cdi, month_years, monthly_contribution)
        lci_lca_value = calculate_lci_lca(investment_value, lci_lca_rentability, cdi, month_years, monthly_contribution)
        savings_value = calculate_savings(investment_value, selic, month_years, monthly_contribution, tr)
        
        cdb_growth.append(cdb_value)
        lci_lca_growth.append(lci_lca_value)
        savings_growth.append(savings_value)
    
    # Obter data inicial
    start_date = datetime.datetime.now()

    # Pandas para pegar o intervalo de meses
    date_range = pd.date_range(start=start_date, periods=len(months), freq='ME')
    month_names = date_range.strftime('%B %Y')

    # Disposição dos dados num dataframe com Pandas para melhor manipulação
    graph_df = pd.DataFrame({
        'Mês': month_names,
        'CDB': cdb_growth,
        'LCI/LCA': lci_lca_growth,
        'Poupança': savings_growth
    })
    
    # Transformando o DataFrame para o formato longo
    graph_df_melted = graph_df.melt(id_vars='Mês', var_name='Tipo de Investimento', value_name='Valor')
    print(graph_df_melted)

    # Plotando o gráfico com plotly.express
    fig = px.line(graph_df_melted, x='Mês', y='Valor', color='Tipo de Investimento',
                labels={'Valor': 'Valor Final (R$)', 'Tipo de Investimento': 'Tipo de Investimento'})

    # Usar eixo Y logarítmico
    fig.update_layout( yaxis=dict(title='Valor Final (R$)', type='log'))

    # Adicionando marcadores para cada ponto
    fig.update_traces(mode='lines+markers', marker=dict(size=6, symbol='circle'))
    
    # Calculando o lucro individual de cada investimento (montante final - investimento inicial - contribuições mensais)
    total_contributions = monthly_contribution * (len(months)-1)

    cdb_profit = cdb_growth[-1] - investment_value - total_contributions
    lci_lca_profit = lci_lca_growth[-1] - investment_value - total_contributions
    savings_profit = savings_growth[-1] - investment_value - total_contributions

    # Calculando o valor total investido
    total_investido = investment_value + total_contributions

    # Criando o DataFrame para comparar investimentos
    result_df = pd.DataFrame({
        'Tipo de Investimento': ['CDB', 'LCI/LCA', 'Poupança'],
        'Investimento Inicial (R$)': [investment_value] * 3,
        'Aportes Mensais (R$)': [total_contributions] * 3,
        'Lucro Final (R$)': [cdb_profit, lci_lca_profit, savings_profit],
        'Valor Total (R$)': [cdb_growth[-1], lci_lca_growth[-1], savings_growth[-1]]
    })

    # Customizando a exibição para destacar o melhor investimento
    def highlight_max(s):
        return ['font-weight: bold; color: green' if v == s.max() else '' for v in s]

    st.dataframe(result_df.style.apply(highlight_max, subset=['Lucro Final (R$)', 'Valor Total (R$)'])
                 .format({col: "{:.2f}" for col in result_df.select_dtypes(include='number').columns}), use_container_width=False)
    
    # Mostrando o gráfico do plotly com o Streamlit
    st.plotly_chart(fig, use_container_width=True, theme=None)
