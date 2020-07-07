def ler_config(arq):
    l = list()  # Lista
    arquivo = open(arq, 'r')
    for linha in arquivo:  # Criar lista com todas as linhas preparadas
        l.append(preparar_linha(linha))
    arquivo.close()
    return l


def preparar_linha(linha):
    linha = linha.split(':')[1]  # Pegar apenas a parte númerica apos split
    linha = linha.split()  # Separar em lista cada valor
    linha_int = [int(item) for item in linha]  # Transformar 'str' em 'int'
    return linha_int


def constroi_matriz(l1, l2):
    l = list()  # Lista
    l.append(l1)
    l.append(l2)
    return l


def fastest_way(a, e):
    '''
  Função que descobre caminho mais rápido entre duas linhas de produção.
    : param a:
    : param t:
    : param e:
    : param x:
    : param n:
    : return :
    '''
    f1 = list()
    f2 = list()

    f1.append(e[0] + a[0][0])
    f2.append(e[1] + a[1][0])
    print(f'{f1} e {f2}')


# Programa Principal ========================================================
import random
lista = ler_config('config.txt')
e = tuple(lista[0])  # CUSTO ENTRADA
a = constroi_matriz(lista[1], lista[4])  # CUSTO CADA ESTACAO
t = constroi_matriz(lista[2], lista[3])  # CUSTO TRANSFERENCIA ENTRE ESTACAO
x = tuple(lista[5])  # CUSTO SAIDA
fastest_way(a, e)
print(f'{e} ----- {a} ----- {t} ----- {x}')
