import streamlit as st
import requests
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Função para buscar dados do fundo imobiliário a partir da API
def get_fii_data(fii_ticker):
    url = f'https://brapi.dev/api/quote/{fii_ticker}?token=xzRG8qbftbU8QaUrd1qRUR'
    response = requests.get(url)
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        return data['results'][0]  # Retorna o primeiro resultado
    else:
        st.error('Erro ao buscar dados do fundo imobiliário.')
        return None

# Função para calcular retorno simulado com reinvestimento de dividendos e compra de cotas mensais
def calculate_compound_return(price, dy, num_shares, monthly_shares, months):
    monthly_return_rate = (dy / 12)  # DY anualizado convertido para taxa de retorno mensal

    total_investment = price * num_shares
    investment_values = []
    monthly_returns = []
    total_shares = num_shares

    for month in range(1, months + 1):
        monthly_return = total_investment * monthly_return_rate
        total_investment += monthly_return + (monthly_shares * price)
        total_shares += monthly_shares + (monthly_return / price)  # Reinvestindo dividendos em mais cotas
        investment_values.append(total_investment)
        monthly_returns.append(monthly_return)
    
    return {
        "investment_values": investment_values,
        "monthly_returns": monthly_returns,
        "total_shares": total_shares,
        "final_value": total_investment
    }

# Função para formatar valores no eixo y
def currency_format(x, _):
    return f'R$ {x:,.2f}'

# Função para plotar gráfico com valores exatos ao passar o cursor
def plot_graph(investment_values, monthly_returns, months, labels):
    months_list = list(range(1, months + 1))

    plt.figure(figsize=(12, 6))
    for investment_value, monthly_return, label in zip(investment_values, monthly_returns, labels):
        plt.plot(months_list, investment_value, marker='o', label=f'Investimento - {label}')
        plt.plot(months_list, monthly_return, marker='x', linestyle='--', label=f'Retorno Mensal - {label}')
    
    plt.title('Comparativo de Fundos Imobiliários com Juros Compostos')
    plt.xlabel('Meses')
    plt.ylabel('Valor (R$)')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(currency_format))
    plt.xticks(rotation=45)
    plt.legend()

    # Adicionando os valores exatos no gráfico
    for i, (investment_value, monthly_return) in enumerate(zip(investment_values, monthly_returns)):
        plt.text(i + 1, investment_value[-1], f'R$ {investment_value[-1]:,.2f}', ha='center', va='bottom', fontsize=8)
        plt.text(i + 1, monthly_return[-1], f'R$ {monthly_return[-1]:,.2f}', ha='center', va='top', fontsize=8)

    st.pyplot(plt)

# Interface do Streamlit
st.title('Simulador de Comparação de Fundos Imobiliários')

st.markdown("**Para obter dados sobre fundos imobiliários, como DY e preço atual, visite:** [https://fiis.com.br/](https://fiis.com.br/)")

num_fundos = st.number_input('Digite o número de fundos imobiliários que deseja comparar:', min_value=1, max_value=10, value=1)

fundos_data = []
for i in range(num_fundos):
    st.subheader(f'Fundo {i+1}')
    ticker = st.text_input(f'Ticker do fundo {i+1} (ex: MXRF11):', key=f'ticker_{i}')
    dy = st.number_input(f'DY (Dividend Yield) do fundo {i+1} (%)', min_value=0.0, max_value=100.0, key=f'dy_{i}')
    price = st.number_input(f'Valor da cota do fundo {i+1} (R$):', min_value=0.0, key=f'price_{i}')
    num_shares = st.number_input(f'Quantidade de cotas iniciais do fundo {i+1}:', min_value=0, key=f'shares_{i}')
    monthly_shares = st.number_input(f'Quantidade de cotas mensais a comprar do fundo {i+1}:', min_value=0, key=f'monthly_shares_{i}')
    if ticker and dy is not None and price and num_shares is not None:
        fundos_data.append((ticker, dy / 100, price, num_shares, monthly_shares))

months = st.number_input('Digite a quantidade de meses para a simulação:', min_value=1, max_value=120, value=12)

if st.button('Simular'):
    investment_values = []
    monthly_returns = []
    total_shares_list = []
    labels = []

    for ticker, dy, price, num_shares, monthly_shares in fundos_data:
        results = calculate_compound_return(price, dy, num_shares, monthly_shares, months)
        investment_values.append(results['investment_values'])
        monthly_returns.append(results['monthly_returns'])
        total_shares_list.append(results['total_shares'])
        labels.append(ticker)
    
    if investment_values:
        plot_graph(investment_values, monthly_returns, months, labels)

    st.subheader('Resultado da projeção reinvestindo dividendo')
    for i, label in enumerate(labels):
        st.write(f"**{label}:**")
        st.write(f"Valor final do investimento: R$ {investment_values[i][-1]:,.2f}")
        st.write(f"Número total de cotas adquiridas: {total_shares_list[i]:,.2f}")
