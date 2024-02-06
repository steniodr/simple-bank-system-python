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

def depositar(saldo, extrato, /):
    menu = '''
    =========== SISTEMA BANCÁRIO SIMPLE BANK ===========
    =                    DEPÓSITO                      =
    =                                                  =
    =                                                  =
    =         INFORME O VALOR A SER DEPOSITADO         =
    =                                                  =
            '''
    
    deposito = float(input(textwrap.dedent(menu)))
    
    if deposito > 0:
        saldo += deposito
        date = get_date()
        print(textwrap.dedent(f'= DEPÓSITO REALIZADO: {deposito:.2f} {date} ='))
        extrato += f'= DEPÓSITO REALIZADO: {deposito:.2f} {date} =\n'
    else:
        print(textwrap.dedent('=  OPERAÇÃO INVALIDA! FAVOR INFORMAR VALOR VÁLIDO  ='))
    
    return saldo, extrato

def sacar(*, saldo, extrato, limite, num_saque, limite_saque):
    menu = '''
    =========== SISTEMA BANCÁRIO SIMPLE BANK ===========
    =                       SAQUE                      =
    =                                                  =
    =                                                  =
    =           INFORME O VALOR A SER SACADO           =
    =                                                  =
            '''

    saque = float(input(textwrap.dedent(menu)))
    
    if saque > saldo:
        print(textwrap.dedent('=  OPERAÇÃO INVALIDA! SAQUE MAIOR QUE SALDO ATUAL  ='))

    elif saque > limite:
        print(textwrap.dedent('=  OPERAÇÃO INVALIDA! SAQUE MAIOR QUE LIMITE ATUAL ='))

    elif num_saque >= limite_saque:
        print(textwrap.dedent('=   OPERAÇÃO INVALIDA! NUMERO DE SAQUES EXCEDIDO   ='))

    elif saque > 0:
        saldo -= saque
        date = get_date()
        print(textwrap.dedent(f'=   SAQUE REALIZADO: {saque:.2f} {date}  ='))
        extrato += f'=   SAQUE REALIZADO: {saque:.2f} {date}  =\n'
        num_saque += 1

    else:
        print(textwrap.dedent('=  OPERAÇÃO INVALIDA! FAVOR INFORMAR VALOR VÁLIDO  ='))

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato,  num_saque, limite_saque):
    print(textwrap.dedent('''
    =========== SISTEMA BANCÁRIO SIMPLE BANK ===========
    =                      EXTRATO                     =
    =                                                  =
    =                                                  ='''))
    print(textwrap.dedent('=                 SEM MOVIMENTAÇÕES                =' if not extrato else extrato))
    
    print(textwrap.dedent(f'''
    =              SALDO ATUAL: {saldo:.2f}                 =
    =          NUMERO DE SAQUES DIPONIVEIS: {limite_saque - num_saque}          =
    ======================= V1 =========================
    '''))

def criar_usuario(usuarios):
    menu = '''
    =========== SISTEMA BANCÁRIO SIMPLE BANK ===========
    =                   CRIAR USUÁRIO                  =
    =                                                  =
    =                                                  =
    =          INFORME O CPF (NUMEROS E PONTOS)        =
    =                                                  =
    '''
    
    cpf = input(textwrap.dedent(menu))
    if valida_cpf(cpf):
        usuario = filtrar_usuario(cpf, usuarios)

        if usuario:
            print(textwrap.dedent('=        OPERAÇÃO INVALIDA! USUÁRIO JÁ CRIADO      ='))
            return

        nome = input(textwrap.dedent('=              INFORME O NOME COMPLETO             =\n'))
        dt_nasc = input(textwrap.dedent('=     INFORME A DATA DE NASCIMENTO (dd/mm/YYYY)    =\n'))
        endereco = input(textwrap.dedent('=            INFORME O ENDEREÇO COMPLETO           =\n'))

        date = get_date()
        numbers_list = [int(digit) for digit in cpf if digit.isdigit()]
        numbers = int(''.join(str(x) for x in numbers_list))

        usuarios.append({'nome': nome, 'data_nascimento': dt_nasc, 'cpf': numbers, 'endereco': endereco})
        print(textwrap.dedent(f'=   USUÁRIO CRIADO: {nome} {date}  ='))

    else:
        print(textwrap.dedent('=          OPERAÇÃO INVALIDA! CPF INVALIDO         ='))
        return criar_usuario(usuarios)

def filtrar_usuario(cpf, usuarios):
    numbers_list = [int(digit) for digit in cpf if digit.isdigit()]
    numbers = int(''.join(str(x) for x in numbers_list))

    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == numbers]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, num_conta, usuarios):
    menu = '''
    =========== SISTEMA BANCÁRIO SIMPLE BANK ===========
    =                   NOVA CONTA                  =
    =                                                  =
    =                                                  =
    =          INFORME O CPF (NUMEROS E PONTOS)        =
    =                                                  =
    '''
    cpf = input(textwrap.dedent(menu))
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        date = get_date()
        print(textwrap.dedent(f'=   CONTA CRIADA:  {date}  ='))
        print(textwrap.dedent(f'    =  AGENCIA: {agencia} - CONTA: {num_conta} - USUÁRIO: {usuario.nome}  ='))

        return {'agencia': agencia, 'numero_conta': num_conta, 'usuario': usuario}
    
    print(textwrap.dedent('=     OPERAÇÃO INVALIDA! USUARIO NÃO ENCONTRADO    ='))

def listar_contas(contas):
    menu = '''
        =========== SISTEMA BANCÁRIO SIMPLE BANK ===========
        =                 LISTA DE CONTAS                  =
        =                                                  =
        =                                                  ='''
    
    print(textwrap.dedent(menu))

    if len(contas) > 0:
        for conta in contas:
            linha = f'''
        =  AGENCIA: {conta['agencia']} - CONTA: {conta['numero_conta']} - TITULAR: {conta['usuario']['nome']}  =')'''
            
        print(textwrap.dedent('=========================++========================='))
        print(textwrap.dedent(linha))
    
    else:
        print(textwrap.dedent('\t=     OPERAÇÃO INVALIDA! CONTAS NÃO ENCONTRADAS    ='))


def main():
    LIMITE_SAQUE = 3
    AGENCIA = '00023'

    saldo = 0
    limite = 500
    extrato = ''
    num_saque = 0
    usuarios = []
    contas = []

    while True:
        fake_load('INICIANDO SISTEMA SIMPLE BANK...')
        opcao = exibir_menu()
        print('\n')
        if opcao.upper() == 'D':
            fake_load("NAVEGANDO PARA A OPÇÃO 'DEPÓSITO'", 0.1)

            saldo, extrato = depositar(saldo, extrato)

        elif opcao.upper() == 'S':
            fake_load("NAVEGANDO PARA A OPÇÃO 'SAQUE'", 0.1)
            

            saldo, extrato = sacar(saldo=saldo, extrato=extrato, limite=limite, num_saque=num_saque, limite_saque=LIMITE_SAQUE)

        elif opcao.upper() == 'E':
            fake_load("NAVEGANDO PARA A OPÇÃO 'EXTRATO'", 0.1)

            exibir_extrato(saldo, extrato=extrato, num_saque=num_saque, limite_saque=LIMITE_SAQUE)

        elif opcao.upper() == 'NU':
            fake_load("NAVEGANDO PARA A OPÇÃO 'NOVO USUÁRIO'", 0.1)
            criar_usuario(usuarios)
        
        elif opcao.upper() == 'NC':
            fake_load("NAVEGANDO PARA A OPÇÃO 'NOVA CONTA'", 0.1)
            num_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, num_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao.upper() == 'LC':
            fake_load("NAVEGANDO PARA A OPÇÃO 'LISTAR CONTAS'", 0.1)
            listar_contas(contas)
        
        elif opcao.upper() == 'Q':
            fake_load("ENCERRANDO SISTEMA", 0.1)
            break

        else:
            print(' # OPERAÇÃO INVALIDA! POR FAVOR SELECIONE UMA OPÇÃO VALIDA...')


main()