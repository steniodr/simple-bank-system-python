import time, sys

from datetime import datetime

animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]



def fake_load(titulo, time_ms = 0.2):

    print(f'\t\t{titulo}\n')



    for i in range(len(animation)):

        time.sleep(time_ms)

        sys.stdout.write('\r' + animation[i % len(animation)])

        sys.stdout.flush()

   

    sys.stdout.write("\r                                    ")



def get_date():

    date = datetime.now()

    current_date = date.strftime('%d/%m/%Y - %H:%M:%S')

    return current_date



menu = '''

        =========== SISTEMA BANCÁRIO SIMPLE BANK ===========

        =                                                  =

        =                 [D] = DEPÓSITO                   =

        =                 [S] = SACAR                      =

        =                 [E] = EXTRATO                    =

        =                 [Q] = SAIR                       =

        =                                                  =

        ======================= V1 =========================



        ESCOLHA A OPÇÃO DESEJADA:

'''



saldo = 0

limite = 500

extrato = ''

num_saque = 0

LIMITE_SAQUE = 3



while True:

    fake_load('INICIANDO SISTEMA SIMPLE BANK...')



    opcao = input(menu)

    print('\n')



    if opcao.upper() == 'D':

        fake_load("NAVEGANDO PARA A OPÇÃO 'DEPÓSITO'", 0.1)

        print('''

        =========== SISTEMA BANCÁRIO SIMPLE BANK ===========

        =                    DEPÓSITO                      =

        =                                                  =

        =                                                  =

        =         INFORME O VALOR A SER DEPOSITADO         =

        =                                                  =

        ''')

        deposito = float(input())



        if deposito > 0:

            saldo += deposito



            date = get_date()

            print(f'\t= DEPÓSITO REALIZADO: {deposito:.2f} {date} =')

            extrato += f'\t= DEPÓSITO REALIZADO: {deposito:.2f} {date} =\n'

       

        else:

            print('=  OPERAÇÃO INVALIDA! FAVOR INFORMAR VALOR VÁLIDO  =')



    elif opcao.upper() == 'S':

        fake_load("NAVEGANDO PARA A OPÇÃO 'SAQUE'", 0.1)

        print('''

        =========== SISTEMA BANCÁRIO SIMPLE BANK ===========

        =                       SAQUE                      =

        =                                                  =

        =                                                  =

        =           INFORME O VALOR A SER SACADO           =

        =                                                  =

        ''')

        saque = float(input())



        if saque > saldo:

            print('\t=  OPERAÇÃO INVALIDA! SAQUE MAIOR QUE SALDO ATUAL  =')

        elif saque > limite:

            print('\t=  OPERAÇÃO INVALIDA! SAQUE MAIOR QUE LIMITE ATUAL =')

        elif num_saque >= LIMITE_SAQUE:

            print('\t=   OPERAÇÃO INVALIDA! NUMERO DE SAQUES EXCEDIDO   =')

        elif saque > 0:

            saldo -= saque

            date = get_date()

            print(f'\t=   SAQUE REALIZADO: {saque:.2f} {date}  =')

            extrato += f'\t=   SAQUE REALIZADO: {saque:.2f} {date}  =\n'

            num_saque += 1

        else:

            print('=  OPERAÇÃO INVALIDA! FAVOR INFORMAR VALOR VÁLIDO  =')



    elif opcao.upper() == 'E':

        fake_load("NAVEGANDO PARA A OPÇÃO 'EXTRATO'", 0.1)

        print('''

        =========== SISTEMA BANCÁRIO SIMPLE BANK ===========

        =                      EXTRATO                     =

        =                                                  =

        =                                                  =''')

        print('=                 SEM MOVIMENTAÇÕES                =' if not extrato else extrato)

        print(f'''

        =              SALDO ATUAL: {saldo:.2f}                 =

        =          NUMERO DE SAQUES DIPONIVEIS: {LIMITE_SAQUE - num_saque}          =

        ======================= V1 =========================

        ''')

       

    elif opcao.upper() == 'Q':

        fake_load("ENCERRANDO SISTEMA", 0.1)

        break

    else:

        print(' # OPERAÇÃO INVALIDA! POR FAVOR SELECIONE UMA OPÇÃO VALIDA...')
