from matplotlib import pyplot as plt
from genetica import gerar_individuo, comprimento
from fitness import fitness
from selecao import roleta_tendenciosa, selecionar_melhores, torneio_binario
from crossover import crossover
from mutar import mutar
from alg_genetico import algoritmo_genetico, salvar_csv_geracao

def gerar_populacao(tamanho_pop, tamanho_individuo):
    populacao = []
    for _ in range(tamanho_pop):
        individuo = gerar_individuo(tamanho_individuo)
        populacao.append(individuo)
    return populacao

def dna_valido(seq):
    # Exemplo de regra gramatical: apenas caracteres A, T, C, G e sem repetições de 3 iguais
    import re
    if not re.fullmatch(r'[ATCG]+', seq):
        return False
    if re.search(r'(A{3,}|T{3,}|C{3,}|G{3,})', seq):
        return False
    return True

alvo = "ATCGTAGGCTA"
if not dna_valido(alvo):
    raise ValueError(f"Sequência alvo inválida para as regras gramaticais: {alvo}")
elite = 2
tamanho = comprimento(alvo)
populacao = gerar_populacao(5, tamanho)

# Após gerar a população inicial, salva CSV da geração 0
salvar_csv_geracao(populacao, alvo, 0, 'pop_geracao_0.csv')

resultado, historico = algoritmo_genetico(
    alvo,
    roleta_tendenciosa,
    tamanho_pop=30,
    taxa_mutacao=0.05,
    max_geracoes=200,
    elite=10,
    verbose_interval=25,
    salvar_csv=True  # Gera todas_geracoes_roleta.csv
)

resultado_torneio, historico_torneio = algoritmo_genetico(
    alvo,
    torneio_binario,
    tamanho_pop=30,
    taxa_mutacao=0.05,
    max_geracoes=200,
    elite=10,
    verbose_interval=25,
    salvar_csv=True  # Gera todas_geracoes_torneio.csv
)

print("="*75)
print("                SIMULAÇÃO DE ALGORITMO GENÉTICO")
print("                   Problema: Correspondência de Sequência DNA")
print("="*75)

print("\nCONFIGURAÇÃO DO EXPERIMENTO:")
print("-" * 45)
print(f"  - Sequência Alvo: {alvo}")
print(f"  - Comprimento: {tamanho} nucleotídeos")
print(f"  - Tamanho da População: 30 indivíduos")
print(f"  - Taxa de Mutação: 5%")
print(f"  - Máximo de Gerações: 200")
print(f"  - Elite: 10 indivíduos")

print("\nANÁLISE DA POPULAÇÃO INICIAL:")
print("-" * 45)
fitness_inicial = []
for i, individuo in enumerate(populacao[:5], 1):
    f = fitness(individuo, alvo)
    fitness_inicial.append(f)
    taxa_acerto = (f/tamanho)*100
    print(f"  {i}. {individuo} - {f:2d}/{tamanho} ({taxa_acerto:5.1f}%)")

media_inicial = sum(fitness_inicial) / len(fitness_inicial)
print(f"\n  Fitness médio inicial: {media_inicial:.2f}/{tamanho} ({media_inicial/tamanho*100:.1f}%)")

print("\n� OPERADORES EVOLUTIVOS - DEMONSTRAÇÃO:")
print("-" * 45)

melhores = roleta_tendenciosa(populacao, alvo, elite)
print(f"  1. SELEÇÃO (Roleta Tendenciosa):")
for i in range(min(2, comprimento(melhores))):
    f = fitness(melhores[i], alvo)
    print(f"     Genitor {i+1}: {melhores[i]} (fitness: {f})")

filho = crossover(melhores[0], melhores[1])
print(f"\n  2. CROSSOVER (Recombinação):")
print(f"     Genitor A: {melhores[0]}")
print(f"     Genitor B: {melhores[1]}")
print(f"     Offspring: {filho}")

mutado = mutar(filho, 0.05)
print(f"\n  3. MUTAÇÃO (Taxa: 5%):")
print(f"     Original:  {filho}")
print(f"     Mutado:    {mutado}")
if filho != mutado:
    print(f"     Status: Mutação aplicada")
else:
    print(f"     Status: Sem mutação nesta iteração")

print(f"\nRESULTADO DA OTIMIZAÇÃO:")
print("-" * 45)

if resultado is not None:
    fitness_final = fitness(resultado, alvo)
    precisao = (fitness_final/tamanho)*100

    print(f"  Sequência Alvo:      {alvo}")
    print(f"  Melhor Solução:      {resultado}")
    print(f"  Fitness Alcançado:   {fitness_final}/{tamanho}")
    print(f"  Precisão:            {precisao:.1f}%")

    if fitness_final == tamanho:
        print(f"  Status: SOLUÇÃO ÓTIMA ENCONTRADA")
        print(f"\n  Correspondência visual:")
        print(f"    Alvo:     {alvo}")
        print(f"    Solução:  {resultado}")
        print(f"    Match:    {''.join('O' if a == b else 'X' for a, b in zip(alvo, resultado))}")
    else:
        print(f"  Status: Solução sub-ótima")
        print(f"\n  Análise de divergência:")
        print(f"    Alvo:     {alvo}")
        print(f"    Solução:  {resultado}")
        print(f"    Match:    {''.join('O' if a == b else 'X' for a, b in zip(alvo, resultado))}")
else:
    print(f"  Status: SOLUÇÃO NÃO ENCONTRADA")
    print(f"  O algoritmo não conseguiu encontrar uma solução adequada")
    print(f"  dentro do limite de {200} gerações.")
    print(f"  Sequência Alvo: {alvo}")
    print(f"  Sugestão: Aumente o número de gerações ou ajuste os parâmetros.")

print(f"\nANÁLISE DE CONVERGÊNCIA:")
print("-" * 45)
print(f"  Fitness inicial: {fitness_inicial[0]} - Fitness final: {fitness_final}")
print(f"  Melhoria absoluta: +{fitness_final - fitness_inicial[0]} pontos")
print(f"  Gerações necessárias: {len(historico)}")
print(f"  Exibindo gráfico de evolução...")

plt.plot(historico, marker='o')
plt.title("Fitness Máxima por Geração")
plt.xlabel("Geração")
plt.ylabel("Fitness")
plt.grid(True)
plt.show()

plt.plot(historico, label='Roleta Tendenciosa')
plt.plot(historico_torneio, label='Torneio Binário')
plt.title("Comparação de Estratégias de Seleção")
plt.xlabel("Geração")
plt.ylabel("Fitness Máxima")
plt.legend()
plt.grid(True)
plt.show()

# Para salvar CSV de cada geração, altere o algoritmo_genetico para incluir a chamada:
# salvar_csv_geracao(populacao, alvo, geracao, f'pop_geracao_{geracao}.csv')
# (Já implementado no alg_genetico.py se solicitado)