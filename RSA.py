from MillerRabin import gerar_primo
import random
import base64

# Calculo de n_aux
def n_aux(p, q):
  return p * q

def valor_phi(p,q):
  return (p-1) * (q-1)

def mdc(a, b):
  # a > b
  while b:
    a, b = b, a % b
  return a

def mdc_extendido(a, b):
  # a > b
  if b == 0:
    return 1, 0, a
  else:
    x, y, mdc = mdc_extendido(b, a % b)
    return y, x -(a // b) *y, mdc
  
def expoente_publico(tamanho_chave, phi):
  while True:
    e = random.randrange(2**tamanho_chave, 2**(tamanho_chave+1)-1)
    if mdc(e, phi):
      return e


def inverso_multiplicativo(e, phi):
  x, y, mdc = mdc_extendido(e, phi)
  if mdc != 1:
    return None
  else:
    return x % phi


def generate_keys():
  tamanho_chave = 12
  p = gerar_primo(tamanho_chave)
  q = gerar_primo(tamanho_chave)
  n = n_aux(p,q)
  phi = valor_phi(p,q)
  print(phi)
  d = None
  while not d:
    e = expoente_publico(tamanho_chave, phi)
    d = inverso_multiplicativo(e, phi)
  print(f"chaves públicas: {n}, {e}")
  print(f"chaves privadas: {p}, {q}, {d}")


def exponenciacao_modular(base, expoente, modulo):
    resultado = 1
    base = base % modulo
    while expoente > 0:
        if expoente % 2 == 1:
           resultado = (resultado * base) % modulo
        expoente = expoente // 2
        base = (base * base) % modulo
    return resultado


def cifrar_RSA(texto,n,e):
  texto_cifrado = [pow(ord(char), e, n) for char in texto]
  return texto_cifrado


def decifrar_RSA(texto,n,d):
  texto_decifrado = [chr(pow(char, d, n)) for char in texto]
  return texto_decifrado

n = 59857871
e = 4133
p = 7517
q = 7963
d = 36429581
texto = "teste"
#texto = "t"
print(cifrar_RSA(texto,n,e))
texto = cifrar_RSA(texto,n,e)
print(decifrar_RSA(texto,n,d))