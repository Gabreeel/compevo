from lcg import randomint

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
    resultado = ''
    for _ in range(tamanho):
        i = randomint(comprimento(alfabeto))
        resultado += caracter_em(alfabeto, i)
    return resultado

