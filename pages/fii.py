import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

# Função para calcular

def calculateProfit(price, dy, numShares, monthlyShares, months):
    monthlyReturnRate = (dy / 12)  # Converte o DY anual para uma taxa de retorno mensal

    totalInvestment = price * numShares  # Calcula o investimento total inicial
    profitValues = []  # Lista para armazenar o lucro acumulado a cada mês
    totalShares = numShares  # Armazena o número total de cotas, começando com as cotas iniciais
    monthlyProfits = []  # Lista para armazenar os lucros mensais
    investmentValues = []  # Lista para armazenar o valor total investido ao longo do tempo

    # Loop para calcular os lucros mês a mês
    for month in range(1, months + 1):
        monthlyReturn = totalInvestment * monthlyReturnRate  # Calcula o retorno mensal
        reinvestedShares = int(monthlyReturn / price)  # Reinveste os dividendos comprando mais cotas inteiras
        totalShares += reinvestedShares + monthlyShares  # Atualiza o número total de cotas
        totalInvestment += monthlyReturn + (monthlyShares * price)  # Atualiza o valor total investido
        profit = totalInvestment - (price * (numShares + monthlyShares * month))  # Calcula o lucro
        profitValues.append(profit)  # Armazena o lucro do mês atual
        monthlyProfits.append(monthlyReturn)  # Armazena o retorno mensal
        investmentValues.append(totalInvestment)  # Armazena o valor investido no mês atual
    
    return profitValues, monthlyProfits, investmentValues  # Retorna as listas de lucros, retornos mensais e valores investidos

# Função para formatar valores no eixo y (em reais)
def currencyFormat(x, _):
    return f'R$ {x:,.2f}'

# Função para plotar gráfico de lucro
def plotProfitGraph(profitValues, monthlyProfits, months, labels):
    monthsList = list(range(1, months + 1))  # Cria uma lista com os números dos meses

    plt.figure(figsize=(12, 6))  # Define o tamanho do gráfico
    for profitValue, monthlyProfit, label in zip(profitValues, monthlyProfits, labels):
        plt.plot(monthsList, profitValue, marker='o', label=f'Lucro - {label}')  # Plota o gráfico de lucro para cada fundo
        for i, (profit, monthly) in enumerate(zip(profitValue, monthlyProfit)):
            plt.text(i + 1, profit, f'R$ {monthly:,.2f}', ha='center', va='bottom', fontsize=8)  # Adiciona rótulos de texto mostrando os retornos mensais
    
    plt.title('Gráfico de Lucro com Reinvestimento de Dividendos')  # Título do gráfico
    plt.xlabel('Meses')  # Rótulo do eixo x
    plt.ylabel('Lucro (R$)')  # Rótulo do eixo y
    plt.gca().yaxis.set_major_formatter(FuncFormatter(currencyFormat))  # Formata o eixo y para mostrar valores em reais
    plt.xticks(rotation=45)  # Rotaciona os rótulos dos meses para melhorar a legibilidade
    plt.legend()  # Exibe a legenda do gráfico

    st.pyplot(plt)  # Mostra o gráfico na interface do Streamlit

# Função para plotar gráfico de investimento ao longo do tempo
def plotInvestmentGraph(investmentValues, months, labels):
    monthsList = list(range(1, months + 1))  # Cria uma lista com os números dos meses

    plt.figure(figsize=(12, 6))  # Define o tamanho do gráfico
    for investmentValue, label in zip(investmentValues, labels):
        plt.plot(monthsList, investmentValue, marker='o', label=f'Investimento - {label}')  # Plota o gráfico de investimento para cada fundo
        for i, investment in enumerate(investmentValue):
            plt.text(i + 1, investment, f'R$ {investment:,.2f}', ha='center', va='bottom', fontsize=8)  # Adiciona rótulos de texto mostrando o valor investido
    
    plt.title('Gráfico de Investimento ao Longo do Tempo')  # Título do gráfico
    plt.xlabel('Meses')  # Rótulo do eixo x
    plt.ylabel('Valor do Investimento (R$)')  # Rótulo do eixo y
    plt.gca().yaxis.set_major_formatter(FuncFormatter(currencyFormat))  # Formata o eixo y para mostrar valores em reais
    plt.xticks(rotation=45)  # Rotaciona os rótulos dos meses para melhorar a legibilidade
    plt.legend()  # Exibe a legenda do gráfico

    st.pyplot(plt)  # Mostra o gráfico na interface do Streamlit

# Interface do Streamlit
st.title('Simulador de Lucro e Investimento de Fundos Imobiliários')  # Título da aplicação

st.markdown("**Para obter dados sobre fundos imobiliários, como DY e preço atual, visite:** [https://fiis.com.br/](https://fiis.com.br/)")  # Link para um site que fornece dados sobre fundos imobiliários

numFundos = st.number_input('Digite o número de fundos imobiliários que deseja comparar:', min_value=1, max_value=10, value=1)  # Input para o número de fundos a serem simulados

fundosData = []  # Lista para armazenar os dados de cada fundo
for i in range(numFundos):
    st.subheader(f'Fundo {i+1}')  # Subtítulo para cada fundo
    ticker = st.text_input(f'Ticker do fundo {i+1} (ex: MXRF11):', key=f'ticker_{i}')  # Input para o ticker do fundo
    dy = st.number_input(f'DY (Dividend Yield) do fundo {i+1} (%)', min_value=0.0, max_value=100.0, key=f'dy_{i}')  # Input para o Dividend Yield do fundo
    price = st.number_input(f'Valor da cota do fundo {i+1} (R$):', min_value=0.0, key=f'price_{i}')  # Input para o valor da cota do fundo
    numShares = st.number_input(f'Quantidade de cotas iniciais do fundo {i+1}:', min_value=0, key=f'shares_{i}')  # Input para a quantidade de cotas iniciais
    monthlyShares = st.number_input(f'Quantidade de cotas mensais a comprar do fundo {i+1}:', min_value=0, key=f'monthly_shares_{i}')  # Input para a quantidade de cotas a comprar mensalmente
    if ticker and dy is not None and price and numShares is not None:
        fundosData.append((ticker, dy / 100, price, numShares, monthlyShares))  # Armazena os dados do fundo na lista

months = st.number_input('Digite a quantidade de meses para a simulação:', min_value=1, max_value=120, value=12)  # Input para a quantidade de meses da simulação

if st.button('Simular'):  # Botão para iniciar a simulação
    profitValues = []  # Lista para armazenar os valores de lucro de todos os fundos
    monthlyProfits = []  # Lista para armazenar os lucros mensais de todos os fundos
    investmentValues = []  # Lista para armazenar os valores investidos de todos os fundos
    labels = []  # Lista para armazenar os tickers dos fundos

    for ticker, dy, price, numShares, monthlyShares in fundosData:
        profits, monthly, investments = calculateProfit(price, dy, numShares, monthlyShares, months)  # Calcula o lucro, retorno mensal e investimento para cada fundo
        profitValues.append(profits)  # Adiciona os lucros à lista
        monthlyProfits.append(monthly)  # Adiciona os retornos mensais à lista
        investmentValues.append(investments)  # Adiciona os valores investidos à lista
        labels.append(ticker)  # Adiciona o ticker do fundo à lista de labels
    
    if profitValues and investmentValues:
        st.subheader("Gráfico de Lucro")  # Subtítulo para o gráfico de lucro
        plotProfitGraph(profitValues, monthlyProfits, months, labels)  # Plota o gráfico de lucro
        
        st.subheader("Gráfico de Investimento ao Longo do Tempo")  # Subtítulo para o gráfico de investimento
        plotInvestmentGraph(investmentValues, months, labels)  # Plota o gráfico de investimento
