seed = 123456789  # semente inicial

# parâmetros da LCG
a = 1103515245
c = 12345
m = 2**31

# gera o próximo número "aleatório"
def next_random():
    global seed
    seed = (a * seed + c) % m
    return seed

# gera número entre 0 e 1
def random01():
    return next_random() / m

# gera inteiro entre 0 e n-1
def randomint(n):
    return int(random01() * n)