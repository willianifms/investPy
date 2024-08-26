import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

# Função para calcular lucro com reinvestimento de dividendos e compra de cotas mensais
def calculateProfit(price, dy, numShares, monthlyShares, months):
    monthlyReturnRate = (dy / 12)  # DY anualizado convertido para taxa de retorno mensal

    totalInvestment = price * numShares
    profitValues = []
    totalShares = numShares
    monthlyProfits = []
    investmentValues = []

    for month in range(1, months + 1):
        monthlyReturn = totalInvestment * monthlyReturnRate
        reinvestedShares = int(monthlyReturn / price)  # Reinvestindo dividendos em cotas inteiras
        totalShares += reinvestedShares + monthlyShares
        totalInvestment += monthlyReturn + (monthlyShares * price)
        profit = totalInvestment - (price * (numShares + monthlyShares * month))
        profitValues.append(profit)
        monthlyProfits.append(monthlyReturn)
        investmentValues.append(totalInvestment)
    
    return profitValues, monthlyProfits, investmentValues

# Função para formatar valores no eixo y
def currencyFormat(x, _):
    return f'R$ {x:,.2f}'

# Função para plotar gráfico de lucro
def plotProfitGraph(profitValues, monthlyProfits, months, labels):
    monthsList = list(range(1, months + 1))

    plt.figure(figsize=(12, 6))
    for profitValue, monthlyProfit, label in zip(profitValues, monthlyProfits, labels):
        plt.plot(monthsList, profitValue, marker='o', label=f'Lucro - {label}')
        for i, (profit, monthly) in enumerate(zip(profitValue, monthlyProfit)):
            plt.text(i + 1, profit, f'R$ {monthly:,.2f}', ha='center', va='bottom', fontsize=8)
    
    plt.title('Gráfico de Lucro com Reinvestimento de Dividendos')
    plt.xlabel('Meses')
    plt.ylabel('Lucro (R$)')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(currencyFormat))
    plt.xticks(rotation=45)
    plt.legend()

    st.pyplot(plt)

# Função para plotar gráfico de investimento ao longo do tempo
def plotInvestmentGraph(investmentValues, months, labels):
    monthsList = list(range(1, months + 1))

    plt.figure(figsize=(12, 6))
    for investmentValue, label in zip(investmentValues, labels):
        plt.plot(monthsList, investmentValue, marker='o', label=f'Investimento - {label}')
        for i, investment in enumerate(investmentValue):
            plt.text(i + 1, investment, f'R$ {investment:,.2f}', ha='center', va='bottom', fontsize=8)
    
    plt.title('Gráfico de Investimento ao Longo do Tempo')
    plt.xlabel('Meses')
    plt.ylabel('Valor do Investimento (R$)')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(currencyFormat))
    plt.xticks(rotation=45)
    plt.legend()

    st.pyplot(plt)

# Interface do Streamlit
st.title('Simulador de Lucro e Investimento de Fundos Imobiliários')

st.markdown("**Para obter dados sobre fundos imobiliários, como DY e preço atual, visite:** [https://fiis.com.br/](https://fiis.com.br/)")

numFundos = st.number_input('Digite o número de fundos imobiliários que deseja comparar:', min_value=1, max_value=10, value=1)

fundosData = []
for i in range(numFundos):
    st.subheader(f'Fundo {i+1}')
    ticker = st.text_input(f'Ticker do fundo {i+1} (ex: MXRF11):', key=f'ticker_{i}')
    dy = st.number_input(f'DY (Dividend Yield) do fundo {i+1} (%)', min_value=0.0, max_value=100.0, key=f'dy_{i}')
    price = st.number_input(f'Valor da cota do fundo {i+1} (R$):', min_value=0.0, key=f'price_{i}')
    numShares = st.number_input(f'Quantidade de cotas iniciais do fundo {i+1}:', min_value=0, key=f'shares_{i}')
    monthlyShares = st.number_input(f'Quantidade de cotas mensais a comprar do fundo {i+1}:', min_value=0, key=f'monthly_shares_{i}')
    if ticker and dy is not None and price and numShares is not None:
        fundosData.append((ticker, dy / 100, price, numShares, monthlyShares))

months = st.number_input('Digite a quantidade de meses para a simulação:', min_value=1, max_value=120, value=12)

if st.button('Simular'):
    profitValues = []
    monthlyProfits = []
    investmentValues = []
    labels = []

    for ticker, dy, price, numShares, monthlyShares in fundosData:
        profits, monthly, investments = calculateProfit(price, dy, numShares, monthlyShares, months)
        profitValues.append(profits)
        monthlyProfits.append(monthly)
        investmentValues.append(investments)
        labels.append(ticker)
    
    if profitValues and investmentValues:
        st.subheader("Gráfico de Lucro")
        plotProfitGraph(profitValues, monthlyProfits, months, labels)
        
        st.subheader("Gráfico de Investimento ao Longo do Tempo")
        plotInvestmentGraph(investmentValues, months, labels)
