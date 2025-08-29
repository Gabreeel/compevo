from genetica import comprimento, caracter_em, alfabeto
from lcg import randomint, random01

def mutar(individuo, taxa_mutacao):
    tamanho = int(comprimento(individuo))

    tamanho_alfabeto = int(comprimento(alfabeto))
    mutado = ''

    for i in range(tamanho):
        if random01() < taxa_mutacao:
            novo = caracter_em(alfabeto, randomint(tamanho_alfabeto))
            mutado += novo
        else:
            mutado += caracter_em(individuo, i)
    return mutado