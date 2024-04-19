from abc import ABC, abstractmethod



# Modelagem de Classes
class Client:
    def __init__(self, address: str):
        self.address = address
        self.accounts = []
    
    def transact(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)


class FisicalPerson(Client):
    def __init__(self, name, birthday, cpf, address):
        super().__init__(address)
        self.name = name
        self.birthday = birthday
        self.cpf = cpf


class Account:
    def __init__(self, account_number, client):
        self.__balance = 0.00
        self.__account_number = account_number
        self.__AGENCY = '0001'
        self.__client = client
        self.__extract = Extract()

    @classmethod
    def new_account(cls, client, account_number):
        return cls(account_number, client)

    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, value):
        self.__balance += value

    @property
    def account_number(self):
        return self.__account_number
    
    @property
    def agency(self):
        return self.__AGENCY

    @property
    def client(self):
        return self.__client
    
    @property
    def extract(self):
        return self.__extract

    def withdraw(self, value):
        status = False
        balance = self.balance

        if value < 0.00:
            failure_message('Valores negativos não são permitidos!')
        elif value > balance:
            failure_message('O valor do saque é maior que o valor disponível na conta!')
        else:
            self.balance = -value; print()
            display_title('SAQUE REALIZADO COM SUCESSO!', width=60, char='=', fill_type=' ')
            status = True

        return status

    def deposit(self, value):
        status = False

        if value < 0.00:
            failure_message('Valores negativos não são permitidos!')
        else:
            self.balance = value; print()
            display_title('DEPÓSITO REALIZADO COM SUCESSO!', width=60, char='=', fill_type=' ')
            status = True

        return status


class CurrentAccount(Account):
    def __init__(self, account_number, client, limit=500.00, daily_limit=3):
        super().__init__(account_number, client)
        self.limit = limit
        self.daily_limit = daily_limit

    def withdraw(self, value):
        status = False
        withdrawals_number = len([transaction for transaction in self.extract.transactions if transaction['type'] == Saque.__name__])

        if value > self.limit:
            failure_message(f'O valor máximo para saque é de apenas R${self.limit:.2f}!'.replace('.', ','))
        elif withdrawals_number >= self.daily_limit:
            failure_message(f'O limite de {self.daily_limit} saques diários já foi ultrapassado!')
        else:
            status = super().withdraw(value)

        return status
    
    def __str__(self):
        account_text = f'• Conta Corrente: {self.agency}-{self.account_number}'
        owner_name_text = f'• Titular da Conta: {self.client.name}'
        owner_cpf_text = f'• CPF do Titular: {self.client.cpf}'

        return f'{account_text}\n{owner_name_text}\n{owner_cpf_text}'


class Extract:
    def __init__(self):
        self.__transactions = []

    @property
    def transactions(self):
        return self.__transactions
    
    @transactions.setter
    def transactions(self, data):
        self.__transactions.append(data)

    def add_transaction(self, transaction):
        self.transactions = {'type': transaction.__class__.__name__, 'value': transaction.value}


class Transaction(ABC):
    @property
    @abstractmethod
    def value(self):
        pass

    @classmethod
    @abstractmethod
    def register(cls, account):
        pass


class Deposito(Transaction):
    def __init__(self, value):
        self.__value = value
    
    @property
    def value(self):
        return self.__value

    def register(self, account):
        if account.deposit(self.value):
            account.extract.add_transaction(self)


class Saque(Transaction):
    def __init__(self, value):
        self.__value = value
    
    @property
    def value(self):
        return self.__value
    
    def register(self, account):
        if account.withdraw(self.value):
            account.extract.add_transaction(self)



# Funções de Customização
def horizontal_separator(*, char: str, amount: int):
    print(char * amount)


def display_title(title: str, /, *, width: int, char: str, fill_type: str):
    horizontal_separator(char=char, amount=width)
    print(title.center(width, fill_type))
    horizontal_separator(char=char, amount=width)


def failure_message(msg: str):
    print()
    horizontal_separator(char='∗', amount=60)
    print('∗', end=''); print(msg.center(58, ' '), end=''); print('∗')
    horizontal_separator(char='∗', amount=60)
    print()


def choose_option():
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



# Constante de Mensagem de Erro
ERROR_MESSAGE: str = '[ERRO: VALOR INVÁLIDO]'

# Funções de Tratamento de Dados
def check_deposit():
    while True:
        try:
            deposit = float(input(f'Valor do depósito: R$').strip())
        except (TypeError, ValueError):
            failure_message(ERROR_MESSAGE)
        else:
            break

    return deposit


def check_withdraw():
    while True:
        try:
            withdraw = float(input('Valor do saque: R$').strip())
        except (TypeError, ValueError):
            failure_message(ERROR_MESSAGE)
        else:
            break

    return withdraw


def check_name():
    while True:
        name = str(input('Nome completo: ')).strip().title()

        test_name: str = name.replace(' ', '')
        if not test_name.isalpha():
            failure_message('Insira apenas letras!')
        else:
            break
    
    return name


def check_birth(date: str, index: int):
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


def check_cpf():
    while True:
        try:
            cpf = str(input('Insira o CPF (apenas números): ')
                    .strip().replace('.', '').replace('-', ''))
        except (TypeError, ValueError):
            failure_message(ERROR_MESSAGE)
        else:
            if len(cpf) != 11:
                failure_message('Insira o CPF corretamente!')
            else:
                break

    return cpf


def check_address(address: str, index: int):
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
                    failure_message('Insira a sigla do estado corretamente!')
                else:
                    break
            case _:
                break

    return add


def filter(cpf: str, clients: list):
    filtered_clients = [client for client in clients if client.cpf == cpf]
    return filtered_clients[0] if filtered_clients else None


def get_client_account(client):
    if not client.accounts:
        failure_message('O cliente não possui contas!')
        return

    return client.accounts[0]



# Funções de Processamento
def create_client(clients: list):
    birthday = address = ''

    cpf = check_cpf()
    client = filter(cpf, clients)

    if client:
        failure_message('Cliente já cadastrado!')
        return

    print(); display_title('INSIRA SEUS DADOS', width=60, char='=', fill_type=' '); print()

    name: str = check_name()

    for i, d in enumerate(['dia', 'mês', 'ano']):
        birth: int = check_birth(d, i)
        birthday += f'{birth}/' if i != 2 else str(birth)

    for j, a in enumerate(['rua', 'número da casa', 'bairro', 'cidade', 'sigla do estado']):
        add: str = check_address(a, j)
        address += f'{add}, ' if j == 0 else f'{add} - ' if 0 < j < 3 else f'{add}/' if j == 3 else add

    client = FisicalPerson(name, birthday, cpf, address)
    clients.append(client)

    print(); display_title('USUÁRIO CRIADO COM SUCESSO!', width=60, char='=', fill_type=' ')


def create_account(account_number: int, clients: list, accounts: list):
    cpf = check_cpf()
    client = filter(cpf, clients)

    if not client:
        failure_message('Cliente não encontrado!')
        return

    account = CurrentAccount.new_account(client, account_number)
    accounts.append(account)
    client.accounts.append(account)

    print(); display_title('CONTA CRIADA COM SUCESSO!', width=60, char='=', fill_type=' ')


def list_accounts(accounts: list):
    display_title('CONTAS CADASTRADAS', width=60, char='=', fill_type=' ')

    for account in accounts:
        print(f'\n{account}')


def deposit(clients: list):
    cpf = check_cpf()
    client = filter(cpf, clients)

    if not client:
        failure_message('Cliente não encontrado!')
        return

    value = check_deposit()
    transaction = Deposito(value)

    account = get_client_account(client)
    if not account:
        return

    client.transact(account, transaction)


def withdraw(clients: list):
    cpf = check_cpf()
    client = filter(cpf, clients)

    if not client:
        failure_message('Cliente não encontrado!')
        return

    value = check_withdraw()
    transaction = Saque(value)

    account = get_client_account(client)
    if not account:
        return

    client.transact(account, transaction)


def show_extract(clients: list):
    cpf = check_cpf()
    client = filter(cpf, clients)

    if not client:
        failure_message('Cliente não encontrado!')
        return
    
    account = get_client_account(client)
    if not account:
        return

    print(); display_title('EXTRATO DA CONTA', width=60, char='=', fill_type=' ')
    transactions = account.extract.transactions

    if not transactions:
        extract = 'Não houveram movimentações na conta!\n'
    else:
        for transaction in transactions:
            extract = f'{transaction["type"]}: R${transaction["value"]:.2f}'.replace('.', ',')
    
    print(extract)
    print(f'Saldo atual: R${account.balance:.2f}'.replace('.', ','))



# Execução do Programa
def main() -> None:
    clients_list: list = []
    accounts_list: list = []
    display_title('Sistema Bancário (V3)', width=60, char='-', fill_type=' ')

    while True:
        option = choose_option()

        match option:
            case 'U':
                create_client(clients_list)
            case 'C':
                account_number = len(accounts_list) + 1
                create_account(account_number, clients_list, accounts_list)
            case 'L':
                list_accounts(accounts_list)
            case 'D':
                deposit(clients_list)
            case 'S':
                withdraw(clients_list)
            case 'E':
                show_extract(clients_list)
            case 'Q':
                print()
                display_title('ATÉ MAIS E VOLTE SEMPRE!', width=60, char='-', fill_type=' ')
                break
            case _:
                failure_message('Opção inválida!')

        horizontal_separator(char='-', amount=60)



if __name__ == '__main__':
    main()
