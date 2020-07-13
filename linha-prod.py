# ===========================================================================
# Variáveis Globais =========================================================
# ===========================================================================

MUL = 40

# ===========================================================================
# Funções ===================================================================
# ===========================================================================


def titulo(texto):
    '''
    Função responsável por criar o título do programa.
    : param texto: texto (string) que deseja alocar no título.
    '''
    print(f'\033[1m\033[1;94m')
    print(f'==' * MUL)
    print(f'{texto:^80}')
    print(f'==' * MUL)
    print(f'\033[m', end='')


def menu():
    '''
    Função responsável por criar o menu de opções e validar a escolha do usuário.
    : return : Retorna a opção do usuário, ou seja, 1 ou 0.
    '''
    while True:
        os.system('cls')
        titulo('LINHA DE MONTAGEM')
        print(f'\033[m')
        print(f'\033[1m1 - Iniciar')
        print(f'0 - Sair')
        try:
            opc = int(input('\n::\033[1;32m '))
        except ValueError as e:
            print(f'\n\033[0;0m\033[31m\033[1mERROR: \033[0;0m\033[;1m{e}\nTente novamente...\033[0;0m')
            time.sleep(1)  # Tempo em segundos
        else:
            if opc in [1, 0]:
                break
            print(f'\n\033[1m\033[31mOpção inválida!\033[0;0m \033[1mTente novamente...\033[0;0m')
            time.sleep(1)

    if opc == 1:
        return True
    else:
        print(f'\n\n\033[1;35m\033[1mOK. Até mais! =D\033[0;0m')
        print('\033[1;34m\033[1m==\033[0;0m' * MUL)
        return False


def ler_arquivo():
    '''
    Função que lê as configurações da linha de montagem, custos da entrada/saída, das estações e das transições.
    : return : Uma matriz (lista de listas) com as configurações.
    '''
    m = list()  # Lista
    while True:
        titulo('LINHA DE MONTAGEM')
        arquivo = input(
            "\nNome do arquivo (default '\033[1;93mconfig.txt\033[0;0m'):\033[1;32m ").strip().lower()
        print(f'\033[0;0m', end='')
        try:
            arq = open(arquivo, 'r')
        except IOError as e:
            print(f"\n\033[1m\033[31mERROR: \033[0;0m\033[1mArquivo '\033[33m{arquivo}\033[0;0m\033[1m' não encontrado...\033[0;0m")
            time.sleep(1)
            os.system('cls')
        else:
            for linha in arq:  # Criar lista com todas as linhas preparadas
                m.append(preparar_linha(linha))
            arq.close()
            return m


def preparar_linha(linha):
    '''
    Função que perara cada linha do arquivo lido para que possa ser usado durante a execução do programa.
    : param linha: Linha que foi lida do arquivo de texto.
    : return : Uma lista com todos os números lidos na linha do arquivo de texto.
    '''
    linha = linha.split(':')[1]  # Pegar apenas a parte númerica apos split
    linha = linha.split()  # Separar em lista cada valor
    linha_int = [int(item) for item in linha]  # Transformar 'str' em 'int'
    return linha_int


def constroi_matriz(lista1, lista2):
    '''
    Função que cria uma lista com dois itens, que também são listase  mesmo tamanho.
    : param lista1: Primeira lista
    : param lista2: Segunda lista
    : return : A matriz (tupla de listas).
    '''
    l = list()
    l.append(lista1)
    l.append(lista2)
    return tuple(l)


def cria_tabuleiro(a, t, e, x, num_estacoes):
    '''
    Função cria uma matriz (tabuleiro) para implementar visualização da rota mais barata.
    : param a: Matriz do custo de cada estação das linhas 0 e 1.
    : param t: Matriz do custo das transferências entre estações (número de estações [n] -1).
    : param e: Tupla do custo de entrada nas linhas 0 e 1.
    : param x: Tupla do custo de saída nas linhas 0 e 1.
    : param num_estacoes: Número de estações
    '''
    # Definindo matrix para viualizar estacoes
    TABLE = np.zeros((4, (num_estacoes * 2) + 1), dtype=int)

    # Definindo valores de entrada e saida
    TABLE[1][0], TABLE[2][0] = e[0], e[1]
    TABLE[1][-1], TABLE[2][-1] = x[0], x[1]

    # Definindo valores intermediarios
    for i in range(len(TABLE)):
        k = p = 0
        for j in range(1, (num_estacoes * 2)):
            if j % 2 == 1:
                TABLE[0][j] = a[0][k]
                TABLE[3][j] = a[1][k]
                k += 1
            elif j % 2 == 0:
                TABLE[1][j] = t[0][p]
                TABLE[2][j] = t[1][p]
                p += 1

    imprime_montagem(TABLE)


def imprime_montagem(TABLE):
    '''
    Função responsável por imprimir na tela o tableiro (matriz).
    : param TABLE: Uma matriz (numpy zeros) em que os custos da linha de montagem e transf. estao alocados.
    '''
    print('\n')
    # Imprimindo linhas de montagem na tela
    arq_saida.write('@ LINHAS DE MONTAGEM\n')
    arq_saida.write('--' * MUL)
    arq_saida.write('\n')
    print(f'\033[;1m@ LINHAS DE MONTAGEM')
    print(f'\033[1m--\033[0;0m' * MUL)
    cont = 1
    for i in range(len(TABLE)):
        time.sleep(0.5)  # Sleep para deixar a animação mais bonita
        if i == 0 or i == 3:
            arq_saida.write('Linha Montagem -> ')
            print(f'\033[1;36mLinha Montagem [{cont}] →\033[0;0m  ', end='')
            cont += 1
        else:
            arq_saida.write('  Custos E/S/T -> ')
            print(f'      \033[1;90mCustos E/S/T →\033[0;0m ', end='')

        for j in range((num_estacoes * 2) + 1):
            if TABLE[i][j] == 0:
                arq_saida.write('--')
                print('--', end='')
            else:
                arq_saida.write(f' {TABLE[i][j]} ')
                print(f' {TABLE[i][j]} ', end='')
        arq_saida.write('\n')
        print()
        if i == 0 or i == 2:
            print()  # Dar um espaço a mais para ficar bonito
    time.sleep(0.5)  # Sleep para deixar a animação mais bonita
    print(f'\033[;1m--\033[0;0m' * MUL)
    arq_saida.write('--' * MUL)


def fastest_way(a, t, e, x, num_estacoes):
    '''
    Função que descobre caminho mais rápido entre duas linhas de montagem.
    : param a: Matriz do custo de cada estação das linhas 0 e 1.
    : param t: Matriz do custo das transferências entre estações (número de estações [n] -1).
    : param e: Tupla do custo de entrada nas linhas 0 e 1.
    : param x: Tupla do custo de saída nas linhas 0 e 1.
    : param num_estacoes: Número de estações
    : return : Menor custo entre as linhas de montagem
    '''

    # Funcao para criar tabuleiro que sera printado no arq. e na tela.
    cria_tabuleiro(a, t, e, x, num_estacoes)

    T1 = [0 for i in range(num_estacoes)]
    T2 = [0 for i in range(num_estacoes)]

    # coloca os valores de entrada e primeira casa
    T1[0] = e[0] + a[0][0]  # Entrada linha 0
    T2[0] = e[1] + a[1][0]  # Entrada linha 1

    # percorre o vetor colocando os valores de cada casa
    for i in range(1, num_estacoes):
        # se linha 1 pega a transição de 1 para 0
        trans = t[1][i - 1]
        custo = a[0][i]
        # resultado é custo da casa atual somado (+) ao minimo entre casa
        # anterior da linha e casa anterior da linha oposta com custo da
        # transição
        if T1[i - 1] <= T2[i - 1] + trans:
            resultado = custo + T1[i - 1]
            R1[i - 1] = 1
        else:
            resultado = custo + T2[i - 1] + trans
            R1[i - 1] = 2
        # grava resultado no vetor de resposta
        T1[i] = resultado

        # se linha 0 pega a transição de 0 para 1
        trans = t[0][i - 1]
        custo = a[1][i]
        if T1[i - 1] + trans <= T2[i - 1]:
            resultado = custo + T1[i - 1] + trans
            R2[i - 1] = 1
        else:
            resultado = custo + T2[i - 1]
            R2[i - 1] = 2
        T2[i] = resultado

    # verificar qual o menor contando com o custo de saida
    if T1[num_estacoes - 1] + x[0] <= T2[num_estacoes - 1] + x[1]:
        tamanho = T1[num_estacoes - 1] + x[0]
        # print("tam1=" + str(tamanho))
        menor = 1
    else:
        tamanho = T2[num_estacoes - 1] + x[1]
        # print("tam2=" + str(tamanho))
        menor = 2

    return tamanho, menor


def imprimir_estacao(menor, estacoes):
    '''
    Função que
    : param menor:
    : param estacoes:
    : return :
    '''

    print(f'\n\n\033[1m@ MELHOR CAMINHO')
    print(f'--' * 20)
    arq_saida.write("\n\n" + '@ MELHOR CAMINHO\n')
    arq_saida.write(f'--' * 20)

    # cria o vetor com o melhor caminho
    linha = menor
    prox_linha = 0
    caminho = list()
    resultado = list()
    # utiliza o vetor de resultados para saber qual o menor caminho entre as casas
    # refaz o caminho do fim ao começo escolhendo as menores distâncias
    for i in range(estacoes, 0, -1):
        # na primeira iteração vai simplesmente salvar 1 ou 2
        # verifica sempre qual a próxima linha a ser visitada para pegar as
        # informações
        if menor == 1 and i == estacoes:
            linha = 1
            prox_linha = R1[i - 2]
        elif menor == 2 and i == estacoes:
            linha = 2
            prox_linha = R2[i - 2]
        elif prox_linha == 1 and i != estacoes:
            linha = prox_linha
            prox_linha = R1[i - 2]
        elif prox_linha == 2 and i != estacoes:
            linha = prox_linha
            prox_linha = R2[i - 2]
        else:
            # caso de errado algo imprime 0 como um erro
            linha = 0
            prox_linha = 0
            return 0
        resultado.append(linha)
        # constroi um vetor com o resultado e uma lista para imprimir
        caminho.append([i, linha])
        # caminho.append(f"estação {i}, linha {linha}")

    # inverte a lista
    caminho.reverse()

    # printa a linha e estação do melhor caminho
    time.sleep(0.5)
    for idx, item in enumerate(caminho):
        if idx == 0:
            # printar entrada
            print(f'\033[0m\033[1;35mEntrada     → Linha {item[1]}\033[0m')
            arq_saida.write(f'\nEntrada     -> Linha {str(item[1])}')
        elif idx == len(caminho) - 1:
            # printar saida
            print(f'\033[1;35mSaída       → Linha {item[1]}\033[0m')
            arq_saida.write(f'\nSaída       -> Linha {str(item[1])}\n')
        else:
            # printar restante das estações
            print(f'Estação [{item[0]}] → Linha {item[1]}')
            arq_saida.write(
                "\n" + "Estação [" + str(item[1]) + "] -> Linha " + str(item[1]))
        time.sleep(0.5)
    print(f'\033[1m--\033[0m' * 20, end='')
    arq_saida.write(f'--' * 20)

    # inverte o vetor, já que ele foi montado do fim ao começo
    return (resultado[::-1])


# ===========================================================================
# Principal =================================================================
# ===========================================================================
import os
import time
import sys
import random
import numpy as np

while True:
    resp = menu()
    if resp:
        os.system('cls')

        lista = ler_arquivo()
        e = tuple(lista[0])  # CUSTO ENTRADA
        a = constroi_matriz(lista[1], lista[4])  # CUSTO CADA ESTACAO
        t = constroi_matriz(lista[2], lista[3])  # CUSTO TRANSFERENCIA
        x = tuple(lista[5])  # CUSTO SAIDA

        arq_saida = open("saida.txt", "w")

        if ((6 <= len(a[0]) <= 10) and (len(a[0]) == len(a[1])) and (len(t[0]) == len(t[1]))):
            num_estacoes = len(a[0])

            R1 = [0 for i in range(num_estacoes - 1)]
            R2 = [0 for i in range(num_estacoes - 1)]

            # chama a função que descobre o melhor caminho
            res = fastest_way(a, t, e, x, num_estacoes)
            # chama a função que printa o melhor caminho
            caminho_final = imprimir_estacao(res[1], num_estacoes)

            # print(f'\n\033[;1mCAMINHO ÓTIMO = {caminho_final}', end="")
            arq_saida.write("\nCAMINHO OTIMO = " + str(caminho_final))

            print(f'\n\033[1m\033[1;32mCUSTO = {res[0]} unidades\033[0m')
            arq_saida.write("\n" + f'MENOR CUSTO = {res[0]} unidades')

        else:
            print(f'\n\033[1m\033[1;31mATENÇÃO:\033[0;0m\033[1m configurações \033[4mnão respeitam\033[0;0m\033[1m o intervalo \033[1m\033[1;31m[6 ~ 10]\033[0;0m \033[1mestações ou estão incorretas.\033[0;0m')
    else:
        break  # sair do programa

    # Verificar se usuário deseja submeter outro arquivo
    opc = input(
        '\n\n\n # Voltar ao menu? [\033[1;32mS\033[0;0m\033[;1m/\033[1;31mN\033[0;0m]: ').lower().strip()[0]
    if opc != 's':
        print(f'\n\n\033[1;35m\033[1m\nOK. Verifique o arquivo "saida.txt"\n\nAté mais! =D\033[0;0m')
        print('\033[1;34m\033[1m==\033[0;0m' * MUL)
        break
