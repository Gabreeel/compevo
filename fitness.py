from genetica import comprimento, caracter_em

def fitness(individuo, alvo):
    acertos = 0
    for i in range(comprimento(alvo)):
        if caracter_em(individuo, i) == caracter_em(alvo, i):
            acertos += 1
    return acertos
