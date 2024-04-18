# Constantes Globais
AGENCY: str = '0001'
VALUE_LIMIT: float = 500.00
ERROR_MESSAGE: str = '[ERRO: VALOR INVÁLIDO]'
NEGATIVE_VALUES: str = 'Valores negativos não são permitidos!'



# Funções de Customização
def horizontal_separator(*, char: str, amount: int) -> None:
    print(char * amount)


def display_title(title: str, /, *, width: int, char: str, fill_type: str) -> None:
    horizontal_separator(char=char, amount=width)
    print(title.center(width, fill_type))
    horizontal_separator(char=char, amount=width)


def choose_option() -> str:
    menu: dict = {'U': 'Criar novo usuário', 'C': 'Criar nova conta', 'L': 'Listar todas as contas',
                  'D': 'Depositar na conta', 'S': 'Sacar da conta', 'E': 'Visualizar extrato', 'Q': 'Sair do programa'}

    print('\nEscolha uma opção:')
    for key, value in menu.items():
        print(f'• [{key}] {value}')

    try:
        option = str(input('\n>>> ')).strip().upper()[0]
    except IndexError:
        option = 'Q'
    
    return option


def failure_message(msg: str) -> None:
    print()
    horizontal_separator(char='∗', amount=60)
    print('∗', end=''); print(msg.center(58, ' '), end=''); print('∗')
    horizontal_separator(char='∗', amount=60)
    print()


def show_data(msg: str, iterable: list[dict]) -> None:
    for i, data in enumerate(iterable):
        print(f'{msg} {i+1} {"{"}')

        for key, value in data.items():
            print(f'  • {key}: {value}')

        print('}')

    print()


# Funções de Tratamento de Dados
def check_deposit() -> float:
    deposit: float

    while True:
        try:
            deposit = float(input(f'Valor do depósito: R$').strip())
        except (TypeError, ValueError):
            failure_message(ERROR_MESSAGE)
        else:
            if deposit < 0.00:
                failure_message(NEGATIVE_VALUES)
            else:
                break

    return deposit


def check_withdraw(balance: float, daily_limit: int) -> float | None:
    withdraw: float

    while True:
        try:
            withdraw = float(input('Valor do saque: R$').strip())
        except (TypeError, ValueError):
            failure_message(ERROR_MESSAGE)
        else:
            if withdraw < 0.00:
                failure_message(NEGATIVE_VALUES)
            elif withdraw > VALUE_LIMIT:
                failure_message(f'O valor máximo para saque é de apenas R${VALUE_LIMIT:.2f}!'.replace('.', ','))
            elif withdraw > balance:
                failure_message('O valor do saque é maior que o valor disponível na conta!')
            else:
                break

    if daily_limit <= 0:
        failure_message('O limite de três saques diários já foi ultrapassado!')
        return

    return withdraw


def check_name() -> str:
    name: str

    while True:
        name = str(input('Nome completo: ')).strip().title()

        test_name: str = name.replace(' ', '')
        if not test_name.isalpha():
            failure_message('Insira apenas letras!')
        else:
            break
    
    return name


def check_birth(date: str, index: int) -> int:
    birth: int

    while True:
        try:
            birth = int(input(f'{date.capitalize()} que nasceu: ').strip())
        except (TypeError, ValueError):
            failure_message(ERROR_MESSAGE)
        else:
            match index:
                case 0:
                    if birth < 1 or birth > 31:
                        failure_message('O dia informado não existe!')
                    else:
                        break
                case 1:
                    if birth < 1 or birth > 12:
                        failure_message('O mês informado não existe!')
                    else:
                        break
                case 2:
                    break

    return birth


def check_cpf() -> int:
    cpf: int

    while True:
        try:
            cpf = int(input('CPF (apenas números): ')
                    .strip().replace('.', '').replace('-', ''))
        except (TypeError, ValueError):
            failure_message(ERROR_MESSAGE)
        else:
            if cpf < 10000000000 or cpf > 99999999999:
                failure_message('Insira o CPF corretamente!')
            else:
                break

    return cpf


def check_address(address: str, index: int) -> str:
    add: str

    while True:
        add = str(input(f'{address.capitalize()} onde mora: ').strip())

        match index:
            case 1:
                if not add.isnumeric():
                    failure_message('Insira apenas números!')
                else:
                    break
            case 4:
                if len(add) != 2:
                    failure_message('Insira a sigla do seu estado corretamente!')
                else:
                    break
            case _:
                break

    return add


def already_exists(users_list: list[dict], cpf: int) -> bool:
    exists: bool = False

    for user in users_list:
        if cpf == user['CPF']:
            exists = True
            break

    return exists



# Funções de Processamento
def create_user(users_list: list[dict]) -> list[dict]:
    birthday = address = ''
    DATE: list[str] = ['dia', 'mês', 'ano']
    ADDRESS: list[str] = ['rua', 'número da casa',
                          'bairro', 'cidade',
                          'sigla do estado']

    print(); display_title('INSIRA SEUS DADOS', width=60, char='=', fill_type=' '); print()

    name: str = check_name()

    for i, d in enumerate(DATE):
        birth: int = check_birth(d, i)
        birthday += f'{birth}/' if i != 2 else str(birth)

    cpf: int = check_cpf()
    if already_exists(users_list, cpf):
        failure_message('CPF já cadastrado!')
        return []

    for j, a in enumerate(ADDRESS):
        add: str = check_address(a, j)
        address += f'{add}, ' if j == 0 else f'{add} - ' if 0 < j < 3 else f'{add}/' if j == 3 else add

    user_info: dict = {'Nome': name, 'Data de Nascimento': birthday,
                       'CPF': cpf, 'Endereço': address}
    users_list.append(user_info)

    print(); display_title('USUÁRIO CRIADO COM SUCESSO!', width=60, char='=', fill_type=' ')

    return users_list


def create_account(agency: str, account_number: int, users_list: list[dict], accounts_list: list[dict]) -> list[dict]:
    current_account: str = f'{agency}-{account_number}'

    while True:
        print('Insira seu ', end='')
        user: int = check_cpf()

        if already_exists(users_list, user):
            break
        else:
            failure_message('Usuário não encontrado!')

    account_info: dict = {'Conta Corrente': current_account, 'CPF do Usuário': user}
    accounts_list.append(account_info)

    print(); display_title('CONTA CRIADA COM SUCESSO!', width=60, char='=', fill_type=' ')

    return accounts_list


def list_accounts(users_list: list[dict], accounts_list: list[dict]) -> None:
    display_title('USUÁRIOS E CONTAS', width=60, char='=', fill_type=' ')

    show_data('Usuário', users_list)
    show_data('Conta', accounts_list)


def deposit(balance: float, extract: str, /) -> tuple[float, str]:
    value = check_deposit()

    balance += value
    extract += f'Depósito: R${value:.2f}\n'.replace('.', ',')

    return balance, extract


def withdraw(*, balance: float, extract: str) -> tuple[float, str]:
    global daily_limit
    value = check_withdraw(balance, daily_limit)

    if value != None:
        daily_limit -= 1
        balance -= value
        extract += f'Saque: R${value:.2f}\n'.replace('.', ',')

    return balance, extract


def show_extract(balance: float, /, *, extract: str) -> None:
    print(); display_title('EXTRATO DA CONTA', width=60, char='=', fill_type=' ')
    print('Não houveram movimentações na conta!\n' if extract == '' else extract)
    print(f'Saldo atual: R${balance:.2f}'.replace('.', ','))



# Adicionando o título
display_title('Sistema Bancário (V2)', width=60, char='-', fill_type=' ')

# Variáveis de Conta
account_number: int = 0
users_list: list[dict] = []
accounts_list: list[dict] = []

# Variáveis Bancárias
balance: float = 0.00
daily_limit: int = 3
extract: str = ''

while True:
    # Criando o menu e escolhendo uma opção
    option = choose_option()

    match option:
        case 'U':
            # Criando e armazenando um novo usuário
            users_list = create_user(users_list)
        case 'C':
            # Criando e armazenando uma nova conta
            account_number += 1
            create_account(AGENCY, account_number, users_list, accounts_list)
        case 'L':
            # Mostrando os usuários e contas criadas
            list_accounts(users_list, accounts_list)
        case 'D':
            # Processando e atribuindo os valores de saldo e extrato
            balance, extract = deposit(balance, extract)
        case 'S':
            # Processando e atualizando os valores de saldo e extrato
            balance, extract = withdraw(balance=balance, extract=extract)
        case 'E':
            # Exibindo o extrato da conta
            show_extract(balance, extract=extract)
        case 'Q':
            # Encerrando a execução do programa
            print()
            display_title('ATÉ MAIS E VOLTE SEMPRE!', width=60, char='-', fill_type=' ')
            break
        case _:
            # Alertando o usuário sobre a invalidez da opção fornecida
            failure_message('Opção inválida!')

    horizontal_separator(char='-', amount=60)
