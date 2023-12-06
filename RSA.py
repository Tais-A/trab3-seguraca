####################################

from MillerRabin import gerar_primo
import random
import base64
from OAEP import aplicar_oaep, remover_oaep
from assinatura import *


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
  tamanho_chave = 1024
  p = gerar_primo(tamanho_chave)
  q = gerar_primo(tamanho_chave)
  n = n_aux(p,q)
  phi = valor_phi(p,q)
  d = None
  while not d:
    e = expoente_publico(tamanho_chave, phi)
    d = inverso_multiplicativo(e, phi)
  chaves_privadas = [n,d]
  chaves_publicas = [n,e]
  print ()
  print(f"Chaves Públicas: \n\n n => {n} \n\n e => {e}\n")
  print(f"Chaves Privadas: \n\n p => {p} \n\n q => {q} \n\n d => {d}\n")
  return ([chaves_privadas,chaves_publicas])


def cifrar_RSA(m,chave):
  n, e = chave
  return pow(m, e, n)


def decifrar_RSA(c,chave):
  n, d = chave
  return pow(c, d, n)
