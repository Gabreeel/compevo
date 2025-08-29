from fitness import fitness
from genetica import comprimento
from lcg import random01

def selecionar_melhores(populacao, alvo, n):
    ordenados = []

    for i in range(comprimento(populacao)):
        inserido = False
        fit_i = fitness(populacao[i], alvo)
        for j in range(comprimento(ordenados)):
            if fit_i > fitness(ordenados[j], alvo):
                ordenados.insert(j, populacao[i])
                inserido = True
                break
        if not inserido:
            ordenados.append(populacao[i])

    selecionados = []
    for i in range(n):
        if i < comprimento(ordenados):
            selecionados.append(ordenados[i])

    return selecionados

def roleta_tendenciosa(populacao, alvo, n):
    fitnesses = []
    total_fitness = 0

    for individuo in populacao:
        fit = fitness(individuo, alvo)
        fitnesses.append(fit)
        total_fitness += fit

    if total_fitness == 0:
        return populacao[:n]
    
    selecionados = []
    for _ in range(n):
        r = random01() * total_fitness
        soma = 0
        for i in range(comprimento(populacao)):
            soma += fitnesses[i]
            if soma >= r:
                selecionados.append(populacao[i])
                break

    return selecionados

def torneio_binario(populacao, alvo, n):
    selecionados = []
    for _ in range(n):
        i1 = int(random01() * len(populacao))
        i2 = int(random01() * len(populacao))
        candidato1 = populacao[i1]
        candidato2 = populacao[i2]
        f1 = fitness(candidato1, alvo)
        f2 = fitness(candidato2, alvo)
        if f1 > f2:
            selecionados.append(candidato1)
        else:
            selecionados.append(candidato2)
    return selecionados
