# ===========================================================================
# Funções ===================================================================
# ===========================================================================


def ler_config(arquivo):
    '''
  Função que lê as configurações da linha de montagem, custos da entrada/saída, das estações e das transições.
    : param arquivo: Arquivo de texto que estão as configurações da linha de montagem.
    : return : Uma matriz (lista de listas) com as configurações.
    '''
    m = list()  # Lista
    file = open(arquivo, 'r')
    for linha in file:  # Criar lista com todas as linhas preparadas
        m.append(preparar_linha(linha))
    file.close()
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
  Função que cria uma lista com dois itens, que também são listas e possuem o mesmo tamanho.
    : param lista1: Primeira lista
    : param lista2: Segunda lista
    : return : A matriz (lista de listas).
    '''
    l = list()
    l.append(lista1)
    l.append(lista2)
    return l


def fastest_way(a, t, e, x, num_estacoes):
    '''
  Função que descobre caminho mais rápido entre duas linhas de produção.
    : param a: Matriz do custo de cada estação das linhas 0 e 1.
    : param t: Matriz do custo das transferências entre estações (número de estações [n] -1).
    : param e: Tupla do custo de entrada nas linhas 0 e 1.
    : param x: Tupla do custo de saída nas linhas 0 e 1.
    : param num_estacoes: Número de estações
    : return : Menor custo entre as linhas de montagem
    '''
    T1 = [0 for i in range(num_estacoes)]
    T2 = [0 for i in range(num_estacoes)]

    # coloca os valores de entrada e primeira casa
    T1[0] = e[0] + a[0][0]  # Entrada linha 0
    T2[0] = e[1] + a[1][0]  # Entrada linha 1

    # percorre o vetor colocando os valores de cada casa
    for i in range(1, num_estacoes):
        # se linha 1 pega a transição de 1 para 0
        trans = t[1][i - 1]
        # resultado é custo da casa atual somado (+) ao minimo entre casa
        # anterior da linha e casa da linha oposta com custo da transição
        resultado = a[0][i] + min(T1[i - 1], T2[i - 1] + trans)
        # grava resultado no vetor de resposta
        T1[i] = resultado

        # se linha 0 pega a transição de 0 para 1
        trans = t[0][i - 1]
        resultado = a[1][i] + min((T1[i - 1] + trans), T2[i - 1])
        T2[i] = resultado

        # verificar qual o menor contando com o custo de saida
        menor = min(T1[num_estacoes - 1] + x[0], T2[num_estacoes - 1] + x[1])

    return menor


# ===========================================================================
# Principal =================================================================
# ===========================================================================
import random
arquivo = 'config.txt'
lista = ler_config(arquivo)
e = tuple(lista[0])  # CUSTO ENTRADA
a = constroi_matriz(lista[1], lista[4])  # CUSTO CADA ESTACAO
t = constroi_matriz(lista[2], lista[3])  # CUSTO TRANSFERENCIA ENTRE ESTACAO
x = tuple(lista[5])  # CUSTO SAIDA
if 6 <= len(a[0]) <= 10:
    num_estacoes = len(a[0])
    result = fastest_way(a, t, e, x, num_estacoes)
    print(f'{result}')
else:
    print(f'O número de estações não respeita o limite! [6 ~ 10]')
    print(f'Verifique seu arquivo "{arquivo}" e tente novamente...')
