from abc import ABC, abstractclassmethod, abstractproperty
import textwrap
import time, sys, re
from datetime import datetime

animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]

def fake_load(titulo, time_ms = 0.2):
    print(f'\t\t{titulo}\n')

    for i in range(len(animation)):
        time.sleep(time_ms)
        sys.stdout.write('\r' + animation[i % len(animation)])
        sys.stdout.flush()
    sys.stdout.write("\r                                    ")

def valida_cpf(cpf):
    # Verifica a formatação do CPF
    if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        return False

    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True

def get_date():
    date = datetime.now()
    current_date = date.strftime('%d/%m/%Y - %H:%M:%S')
    return current_date

class Conta:
    def __init__(self, numero, usuario):
        self.saldo = 0
        self.numero = numero
        self.agencia = "0023"
        self.usuario = usuario
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, usuario, numero):
        return cls(usuario, numero)

    @property
    def saldo(self):
        return self.saldo
    
    @property
    def numero(self):
        return self.numero
    
    @property
    def agencia(self):
        return self.agencia
    
    @property
    def usuario(self):
        return self.usuario

    @property
    def historico(self):
        return self.historico
    
    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print(textwrap.dedent('=  OPERAÇÃO INVALIDA! SAQUE MAIOR QUE SALDO ATUAL  ='))


        elif valor > 0:
            self._saldo -= valor
            date = get_date()
            print(textwrap.dedent(f'=   SAQUE REALIZADO: {valor:.2f} {date}  ='))
            return True

        else:
            print(textwrap.dedent('=  OPERAÇÃO INVALIDA! FAVOR INFORMAR VALOR VÁLIDO  ='))

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            date = get_date()
            print(textwrap.dedent(f'= DEPÓSITO REALIZADO: {valor:.2f} {date} ='))
        else:
            print(textwrap.dedent('=  OPERAÇÃO INVALIDA! FAVOR INFORMAR VALOR VÁLIDO  ='))
            return False

        return True

class ContaCorrente(Conta):
    def __init__(self, numero, usuario, limite=500, limite_saques=3):
        super().__init__(numero, usuario)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print(textwrap.dedent('=   OPERAÇÃO INVALIDA! VALOR DE SAQUE EXCEDE O LIMITE   ='))


        elif excedeu_saques:
            print(textwrap.dedent('=   OPERAÇÃO INVALIDA! NUMERO DE SAQUES EXCEDIDO   ='))

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.usuario.nome}
        """

class Usuario:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Usuario):
    def __init__(self, nome, data_nascimento, cpf, endereco, criacao):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.criacao = criacao

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": get_date(),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def exibir_menu():
    menu = '''
                =========== SISTEMA BANCÁRIO SIMPLE BANK ===========
                =                                                  =
                =                 [D]  = DEPÓSITO                  =
                =                 [S]  = SACAR                     =
                =                 [E]  = EXTRATO                   =
                =                 [NC] = NV. CONTA                 =
                =                 [NU] = NV. USUARIO               =
                =                 [LC] = LT. CONTAS                =
                =                 [Q]  = SAIR                      =
                =                                                  =
                ======================= V1 =========================
                ESCOLHA A OPÇÃO DESEJADA:
    '''
    return input(textwrap.dedent(menu))

def filtrar_usuario(cpf, usuarios):
    numbers_list = [int(digit) for digit in cpf if digit.isdigit()]
    numbers = int(''.join(str(x) for x in numbers_list))

    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == numbers]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def recuperar_conta_usuario(usuario):
    if not usuario.contas:
        print(textwrap.dedent('=  OPERAÇÃO INVALIDA! USUÁRIO NÃO POSSUI CONTA  ='))
        return

    return usuario.contas[0]

def depositar(usuarios):
    cpf = input(textwrap.dedent("=          INFORME O CPF (NUMEROS E PONTOS) DO USUÁRIO       =\n"))
    
    if valida_cpf(cpf):
        usuario = filtrar_usuario(cpf, usuarios)

        if not usuario:
            print(textwrap.dedent('=        OPERAÇÃO INVALIDA! USUÁRIO NÃO ENCONTRADO      ='))
            return

        valor = float(input(textwrap.dedent("=          INFORME O VALOR DO DEPOSITO       =\n")))
        transacao = Deposito(valor)

        conta = recuperar_conta_usuario(usuario)
        if not conta:
            return

        usuario.realizar_transacao(conta, transacao)
    else:
        print(textwrap.dedent('=          OPERAÇÃO INVALIDA! CPF INVALIDO         ='))
        return depositar(usuarios)
    
def sacar(usuarios):
    cpf = input(textwrap.dedent("=          INFORME O CPF (NUMEROS E PONTOS) DO USUÁRIO       =\n"))

    if valida_cpf(cpf):
        usuario = filtrar_usuario(cpf, usuarios)

        if not usuario:
            print(textwrap.dedent('=        OPERAÇÃO INVALIDA! USUÁRIO NÃO ENCONTRADO      ='))
            return

        valor = float(input(textwrap.dedent("=          INFORME O VALOR DO SAQUE       =\n")))
        transacao = Saque(valor)

        conta = recuperar_conta_usuario(usuario)
        if not conta:
            return

        usuario.realizar_transacao(conta, transacao)
    else:
        print(textwrap.dedent('=          OPERAÇÃO INVALIDA! CPF INVALIDO         ='))
        return sacar(usuarios)
    
def exibir_extrato(usuarios):
    cpf = input(textwrap.dedent("=          INFORME O CPF (NUMEROS E PONTOS) DO USUÁRIO       =\n"))
    if valida_cpf(cpf):
        usuario = filtrar_usuario(cpf, usuarios)

        if not usuario:
            print(textwrap.dedent('=        OPERAÇÃO INVALIDA! USUÁRIO NÃO ENCONTRADO      ='))
            return

        conta = recuperar_conta_usuario(usuario)
        if not conta:
            return

        print(textwrap.dedent('''
        =========== SISTEMA BANCÁRIO SIMPLE BANK ===========
        =                      EXTRATO                     =
        =                                                  =
        =                                                  ='''))
        transacoes = conta.historico.transacoes

        extrato = ""
        if not transacoes:
            extrato = "=        NÃO FOI REALIZADO TRANSAÇÕES      ="
        else:
            for transacao in transacoes:
                extrato += f"\n= {transacao['tipo']}:\n\tR$ {transacao['valor']:.2f} ="

        print(textwrap.dedent(extrato))
        print(textwrap.dedent(f"\nSALDO:\n\tR$ {conta.saldo:.2f}"))
        print(textwrap.dedent("======================= V1 ========================="))
    else:
        print(textwrap.dedent('=          OPERAÇÃO INVALIDA! CPF INVALIDO         ='))
        return exibir_extrato(usuarios)

def criar_usuario(usuarios):
    cpf = input(textwrap.dedent('=          INFORME O CPF (NUMEROS E PONTOS) DO USUÁRIO       =\n'))
    if valida_cpf(cpf):
        usuario = filtrar_usuario(cpf, usuarios)

        if usuario:
            print(textwrap.dedent(f'=        OPERAÇÃO INVALIDA! USUÁRIO JÁ CADASTRADO    ='))
            print(textwrap.dedent(f'=        DATA DE CRIAÇÃO: {usuario.criacao}    ='))
            return

        nome =              input(textwrap.dedent('=              INFORME O NOME COMPLETO             =\n'))
        data_nascimento =   input(textwrap.dedent('=     INFORME A DATA DE NASCIMENTO (dd/mm/YYYY)    =\n'))
        endereco =          input(textwrap.dedent('=            INFORME O ENDEREÇO COMPLETO           =\n'))

        date = get_date()
        numbers_list = [int(digit) for digit in cpf if digit.isdigit()]
        numbers = int(''.join(str(x) for x in numbers_list))

        usuario = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=numbers, endereco=endereco, criacao=date)

        usuarios.append(usuario)

        print(textwrap.dedent(f'=   USUÁRIO CRIADO: {nome} - {date}  ='))
    else:
        print(textwrap.dedent('=          OPERAÇÃO INVALIDA! CPF INVALIDO         ='))
        return criar_usuario(usuarios)

def criar_conta(numero_conta, usuarios, contas):
    cpf = input(textwrap.dedent("=          INFORME O CPF (NUMEROS E PONTOS) DO USUÁRIO       =\n"))
    if valida_cpf(cpf):
        usuario = filtrar_usuario(cpf, usuarios)

        if not usuario:
            print(textwrap.dedent('=        OPERAÇÃO INVALIDA! USUÁRIO NÃO ENCONTRADO      ='))
            return

        conta = ContaCorrente.nova_conta(usuario=usuario, numero=numero_conta)
        contas.append(conta)
        usuario.contas.append(conta)

        print(textwrap.dedent(f'=          CONTA CRIADA COM SUCESSO         ='))
    else:
        print(textwrap.dedent('=          OPERAÇÃO INVALIDA! CPF INVALIDO         ='))
        return criar_usuario(usuarios)

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    usuarios = []
    contas = []

    while True:
        fake_load('INICIANDO SISTEMA SIMPLE BANK...')
        opcao = exibir_menu()
        print('\n')
        if opcao.upper() == 'D':
            fake_load("NAVEGANDO PARA A OPÇÃO 'DEPÓSITO'", 0.1)
            depositar(usuarios)

        elif opcao.upper() == 'S':
            fake_load("NAVEGANDO PARA A OPÇÃO 'SAQUE'", 0.1)
            sacar(usuarios)

        elif opcao.upper() == 'E':
            fake_load("NAVEGANDO PARA A OPÇÃO 'EXTRATO'", 0.1)
            exibir_extrato(usuarios)

        elif opcao.upper() == 'NU':
            fake_load("NAVEGANDO PARA A OPÇÃO 'NOVO USUÁRIO'", 0.1)
            criar_usuario(usuarios)
        
        elif opcao.upper() == 'NC':
            fake_load("NAVEGANDO PARA A OPÇÃO 'NOVA CONTA'", 0.1)
            num_conta = len(contas) + 1
            criar_conta(num_conta, usuarios, contas)

        elif opcao.upper() == 'LC':
            fake_load("NAVEGANDO PARA A OPÇÃO 'LISTAR CONTAS'", 0.1)
            listar_contas(contas)
        
        elif opcao.upper() == 'Q':
            fake_load("ENCERRANDO SISTEMA", 0.1)
            break

        else:
            print(' # OPERAÇÃO INVALIDA! POR FAVOR SELECIONE UMA OPÇÃO VALIDA...')

main()