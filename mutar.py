def dna_valido(seq):
    import re
    if not re.fullmatch(r'[ATCG]+', seq):
        return False
    if re.search(r'(A{3,}|T{3,}|C{3,}|G{3,})', seq):
        return False
    return True
from genetica import comprimento, caracter_em, alfabeto
import random

def mutar(individuo, taxa_mutacao):
    tamanho = int(comprimento(individuo))
    tentativas = 0
    while True:
        mutado = ''
        for i in range(tamanho):
            if random.random() < taxa_mutacao:
                base = random.choice(alfabeto)
                # Evita repetições de 3 ou mais
                if i >= 2 and base == mutado[-1] and base == mutado[-2]:
                    base = random.choice([b for b in alfabeto if b != base])
                mutado += base
            else:
                mutado += caracter_em(individuo, i)
        if dna_valido(mutado):
            return mutado
        tentativas += 1
        if tentativas > 10:
            return individuo