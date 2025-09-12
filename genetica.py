def dna_valido(seq):
    import re
    if not re.fullmatch(r'[ATCG]+', seq):
        return False
    if re.search(r'(A{3,}|T{3,}|C{3,}|G{3,})', seq):
        return False
    return True
import random

alfabeto = "ATCG"

def comprimento(s):
    count = 0
    for _ in s:
        count += 1
    return int(count)

def caracter_em(s, i):
    count = 0
    for c in s:
        if count == i:
            return c
        count += 1
    return '' #caso índice fora do intervalo

def gerar_individuo(tamanho):
    while True:
        individuo = ''
        for i in range(tamanho):
            base = random.choice(alfabeto)
            # Evita repetições de 3 ou mais
            if i >= 2 and base == individuo[-1] and base == individuo[-2]:
                base = random.choice([b for b in alfabeto if b != base])
            individuo += base
        if dna_valido(individuo):
            return individuo

