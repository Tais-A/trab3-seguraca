import random

# num = d*(2^r) + 1
def decomposicao(num):
  d = num - 1
  r = 0 
  while d % 2 == 0:
    r += 1
    d //= 2
  return [d,r]


def rabin_miller(num, k = 128):
  #verifica se um num é primo
  d,r = decomposicao(num)

  for _ in range(k):
    a = random.randrange(2, num - 1)
    v = pow(a, d, num)
    if v != 1:
      i = 0
      while v != (num - 1):
        if i == r - 1:
          return False
        else:
          i = i + 1
          v = (v ** 2) % num
    return True

def verifica_primo(num):
  # se for par retorna falso, se não chama a verificação de Miller
  if num & 1 != 0:
    return rabin_miller(num)
  return False

def gerar_primo(tamanho_chave):
  while True:
    num = random.randrange(2**tamanho_chave, 2**(tamanho_chave+1)-1)
    if verifica_primo(num):
      return num
