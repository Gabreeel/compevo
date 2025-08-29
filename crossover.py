from genetica import comprimento, caracter_em
from lcg import randomint

def crossover(pai1, pai2):
    tamanho = comprimento(pai1)
    ponto_corte = randomint(tamanho - 1) + 1
    filho = ''
    for i in range(tamanho):
        if i < ponto_corte:
            filho += caracter_em(pai1, i)
        else:
            filho += caracter_em(pai2, i)
    return filho