investimento_inicial=float(input('Digite o valor inicial do investimento:'))
anos=int(input('Quantos anos será o tipo de investimento?'))
print('Qual Será o tipo de investimento?')
print('1. Cofrinho do inter (Rende 100% do  CDI)')
print('2. Cofrinho do Nubank (Rende 100% do CDI)')
print('3.Cofrinho do PicPay (Rende 102% do CDI)')
escolha=int(input("Digite o numero do banco escolhido:"))
if escolha == 1:
    taxa_de_juros = 0.104
elif escolha == 2:
    taxa_de_juros = 0.104
elif escolha == 3:
    taxa_de_juros = 0.1061
else:
    print('Escolha uma opcao valida!!!')
valor_final = investimento_inicial * (1+taxa_de_juros) ** anos
print(f"O valor final apos {anos} anos sera de: R$ {valor_final:.2f}")