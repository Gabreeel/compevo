from genetica import gerar_individuo, comprimento
from fitness import fitness
from selecao import selecionar_melhores, roleta_tendenciosa, torneio_binario
from crossover import crossover
from mutar import mutar
import random
import re
from matplotlib import pyplot as plt
from matplotlib import cm
import csv

# Função para validar regras gramaticais do DNA
# (deve ser igual à usada nos outros módulos)
def dna_valido(seq):
    if not re.fullmatch(r'[ATCG]+', seq):
        return False
    if re.search(r'(A{3,}|T{3,}|C{3,}|G{3,})', seq):
        return False
    return True

def gerar_populacao(tamanho_pop, tamanho_individuo):
    populacao = []
    for _ in range(tamanho_pop):
        populacao.append(gerar_individuo(tamanho_individuo))
    return populacao

def algoritmo_genetico(alvo, estrategia_selecao, tamanho_pop = 100, taxa_mutacao = 0.05, max_geracoes = 1000, elite = 20, verbose_interval = 20, salvar_csv=False):
    tamanho_individuo = comprimento(alvo)
    populacao = gerar_populacao(tamanho_pop, tamanho_individuo)
    hist_fitness = []
    melhor_global = None
    melhor_fitness_global = -1
    historico_populacoes = [list(populacao)]  # Guarda todas as populações
    
    print(f"\nIniciando evolução - Alvo: {alvo}")
    print(f"   Parâmetros: {max_geracoes} gerações, população {tamanho_pop}, elite {elite}")
    
    for geracao in range(max_geracoes):
        # Seleciona elite de pais usando a estratégia definida
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
            if salvar_csv:
                salvar_csv_todas_geracoes(historico_populacoes, alvo, 'todas_geracoes.csv')
            return melhor, hist_fitness
        
        nova_pop = []
        # Para cada novo indivíduo, seleciona os pais usando a estratégia de seleção
        while comprimento(nova_pop) < tamanho_pop:
            # Seleciona pai1 e pai2 usando a estratégia de seleção, não apenas elite aleatória
            pai1 = estrategia_selecao(populacao, alvo, 1)[0]
            pai2 = estrategia_selecao(populacao, alvo, 1)[0]
            filho = crossover(pai1, pai2)
            # Validação gramatical do filho após crossover
            tentativas = 0
            while not dna_valido(filho) and tentativas < 10:
                pai1 = estrategia_selecao(populacao, alvo, 1)[0]
                pai2 = estrategia_selecao(populacao, alvo, 1)[0]
                filho = crossover(pai1, pai2)
                tentativas += 1
            # Aplica mutação e garante que o resultado também seja válido
            filho = mutar(filho, taxa_mutacao)
            if dna_valido(filho):
                nova_pop.append(filho)
            else:
                # Se não conseguir gerar filho válido, mantém o melhor pai
                nova_pop.append(melhor)
        populacao = nova_pop
        historico_populacoes.append(list(populacao))
    print (f'\nEvolução concluída após {max_geracoes} gerações.')
    print (f'Melhor solução: {melhor_global} (fitness: {melhor_fitness_global}/{tamanho_individuo})')
    if salvar_csv:
        salvar_csv_todas_geracoes(historico_populacoes, alvo, 'todas_geracoes.csv')
    return melhor_global, hist_fitness

def mostrar_populacao_colorida(populacao, alvo):
    fitnesses = [fitness(ind, alvo) for ind in populacao]
    # Normaliza fitness para [0,1]
    norm_fitness = [f / len(alvo) for f in fitnesses]
    # Mapeia para gradiente de cor RdYlGn
    cores = cm.RdYlGn(norm_fitness)
    plt.figure(figsize=(6, len(populacao) * 0.5))
    for i, (ind, cor) in enumerate(zip(populacao, cores)):
        plt.text(0.1, len(populacao)-i, ind, backgroundcolor=cor, fontsize=12)
        plt.text(0.7, len(populacao)-i, f"{fitnesses[i]}/{len(alvo)}", backgroundcolor=cor, fontsize=12)
    plt.text(0.1, 0, f"Alvo: {alvo}", backgroundcolor=cm.RdYlGn(1.0), fontsize=12, fontweight='bold')
    plt.axis("off")
    plt.title("População Inicial - Fitness por Cor")
    plt.show()

def fitness_cor(f, alvo):
    """Retorna cor RGB normalizada para o fitness usando RdYlGn."""
    from matplotlib import cm
    norm = f / len(alvo)
    rgba = cm.RdYlGn(norm)
    # Converte para string RGB (ex: 'rgb(34,139,34)')
    r, g, b, _ = [int(x*255) for x in rgba]
    return f'rgb({r},{g},{b})'

def salvar_csv_geracao(populacao, alvo, geracao, filename):
    """Salva população, fitness, cor e comparação com alvo em CSV."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Geração', 'Indivíduo', 'Fitness', 'Cor', 'Alvo', 'Comparação'])
        for ind in populacao:
            fit = fitness(ind, alvo)
            cor = fitness_cor(fit, alvo)
            comp = ''.join('O' if a == b else 'X' for a, b in zip(alvo, ind))
            writer.writerow([geracao, ind, f'{fit}/{len(alvo)}', cor, alvo, comp])

def salvar_csv_todas_geracoes(historico_populacoes, alvo, filename):
    """Salva todos os indivíduos de todas as gerações, fitness, cor, comparação e fitness médio por geração."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Geração', 'Indivíduo', 'Fitness', 'Cor', 'Alvo', 'Comparação', 'Fitness Médio', 'Fitness Objetivo'])
        for geracao, populacao in enumerate(historico_populacoes):
            fitnesses = [fitness(ind, alvo) for ind in populacao]
            media = sum(fitnesses) / len(fitnesses)
            for ind, fit in zip(populacao, fitnesses):
                cor = fitness_cor(fit, alvo)
                comp = ''.join('O' if a == b else 'X' for a, b in zip(alvo, ind))
                writer.writerow([geracao, ind, f'{fit}/{len(alvo)}', cor, alvo, comp, f'{media:.2f}', f'{len(alvo)}'])

# Exemplo de uso (adicione no app.py após cada geração):
# salvar_csv_geracao(populacao, alvo, geracao, f'pop_geracao_{geracao}.csv')
# Para usar, passe uma lista de populações de cada geração (ex: [pop_0, pop_1, ..., pop_N])
# salvar_csv_todas_geracoes(historico_populacoes, alvo, 'todas_geracoes.csv')
