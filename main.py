# Adicionando o título
print('-' * 60)
print('Sistema Bancário (V2)'.center(60, ' '))
print('-' * 60)

# Criando o menu
menu: str = '''
Escolha uma opção:
[D] Depósito
[S] Saque
[E] Extrato
[Q] Quit (sair)

>>> '''

# Variáveis bancárias
balance: float = 0.00
daily_limit: int = 3
extract: str = ''
dep = saq = 0

while True:
    # Escolhendo uma opção
    try:
        option = str(input(menu)).strip().upper()[0]
    except (IndexError, KeyboardInterrupt):
        option = 'Q'

    match option:
        case 'D':
            # Coletando o valor do depósito
            while True:
                try:
                    deposit = float(input('Insira um valor para depósito: R$').strip())
                except (TypeError, ValueError, KeyboardInterrupt):
                    print(' [ERRO: INSIRA APENAS VALORES INTEIROS] ')
                else:
                    if deposit < 0.00:
                        print('Valores negativos não são permitidos!\n')
                    else:
                        break

            # Adicionando o valor obtido ao saldo
            dep += 1
            balance += deposit
            extract += f'{dep}º Depósito: R${deposit:.2f}\n'.replace('.', ',')
        case 'S':
            # Checando se o limite diário já estourou
            if daily_limit <= 0:
                print(f'O limite de três saques diários já foi ultrapassado!\n{"-" * 60}')
                continue

            # Coletando o valor do saque
            while True:
                try:
                    withdraw = float(input('Insira um valor para saque: R$').strip())
                except (TypeError, ValueError, KeyboardInterrupt):
                    print(' [ERRO: INSIRA APENAS VALORES INTEIROS] ')
                else:
                    if withdraw < 0.00:
                        print('Valores negativos não são permitidos!\n')
                    elif withdraw > 500.00:
                        print('O valor máximo para saque é de apenas R$500,00!\n')
                    elif withdraw > balance:
                        print('O valor do saque é maior que o valor disponível na conta!\n')
                    else:
                        break

            # Removendo do saldo o valor obtido
            saq += 1
            daily_limit -= 1
            balance -= withdraw
            extract += f'{saq}º Saque: R${withdraw:.2f}\n'.replace('.', ',')
        case 'E':
            # Exibindo o extrato da conta
            print('\n' + ' EXTRATO DA CONTA '.center(60, '='))
            print('Não houveram movimentações na conta!\n' if extract == '' else extract)
            print(f'Saldo atual: R${balance:.2f}'.replace('.', ','))
            print('=' * 60)
        case 'Q':
            # Encerrando a execução do programa
            print('\n' + '-' * 60)
            print('ATÉ MAIS E VOLTE SEMPRE!'.center(60, ' '))
            print('-' * 60)
            break
        case _:
            # Alertando o usuário sobre a invalidez da opção fornecida
            print('Opção inválida!')
            print('Selecione apenas: [D] | [S] | [E] | [Q]')

    print('-' * 60)
