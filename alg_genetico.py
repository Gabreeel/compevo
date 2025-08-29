from genetica import gerar_individuo, comprimento
from fitness import fitness
from selecao import selecionar_melhores, roleta_tendenciosa, torneio_binario
from crossover import crossover
from mutar import mutar
from lcg import randomint

def gerar_populacao(tamanho_pop, tamanho_individuo):
    populacao = []
    for _ in range(tamanho_pop):
        populacao.append(gerar_individuo(tamanho_individuo))
    return populacao

def algoritmo_genetico(alvo, estrategia_selecao, tamanho_pop = 100, taxa_mutacao = 0.05, max_geracoes = 1000, elite = 20, verbose_interval = 20):
    tamanho_individuo = comprimento(alvo)
    populacao = gerar_populacao(tamanho_pop, tamanho_individuo)
    hist_fitness = []
    melhor_global = None
    melhor_fitness_global = -1
    
    print(f"\nIniciando evolução - Alvo: {alvo}")
    print(f"   Parâmetros: {max_geracoes} gerações, população {tamanho_pop}, elite {elite}")
    
    for geracao in range(max_geracoes):
        pais = estrategia_selecao(populacao, alvo, elite)
        melhor = max(pais, key=lambda ind: fitness(ind, alvo))
        fit = fitness(melhor, alvo)
        hist_fitness.append(fit)
        
        melhoria_significativa = fit > melhor_fitness_global
        
        if fit > melhor_fitness_global:
            melhor_global = melhor
            melhor_fitness_global = fit

        mostrar = (
            geracao == 0 or
            geracao % verbose_interval == 0 or
            melhoria_significativa or
            geracao == max_geracoes - 1
        )
        
        if mostrar:
            progresso = (fit / tamanho_individuo) * 100
            status = "*" if melhoria_significativa else "-"
            print(f"{status} Geração {geracao:3d}: {melhor} | Fitness: {fit:2d}/{tamanho_individuo} ({progresso:5.1f}%)")

        if fit == tamanho_individuo:
            print('Alvo Atingido!')
            return melhor, hist_fitness
        
        nova_pop = []

        while comprimento(nova_pop) < tamanho_pop:
            pai1 = pais[randomint(elite)]
            pai2 = pais[randomint(elite)]
            filho = crossover(pai1, pai2)
            filho = mutar(filho, taxa_mutacao)
            nova_pop.append(filho)

        populacao = nova_pop

    print (f'\nEvolução concluída após {max_geracoes} gerações.')
    print (f'Melhor solução: {melhor_global} (fitness: {melhor_fitness_global}/{tamanho_individuo})')
    return melhor_global, hist_fitness
