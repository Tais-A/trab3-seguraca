from MillerRabin import gerar_primo_grande

# Gerar chaves utilizadas


# Calculo de n_aux
def n_aux(p, q):
  return p * q

def phi(p,q):
  return (p-1) * (q-1)

def mdc(numero):
  pass

def e():
  pass

def inverso_multiplicativo(e):
  pass


def generate_keys():
  p = gerar_primos_grandes()
  q = gerar_primos_grandes()
  n = n_aux(p,q)
  phi = phi(p,q)
  #e =
  print(f"chaves públicas: {n}, {e}")
  print(f"chaves privadas: {p}, {q}, {d}")


def cifrar_RSA(n,e):
  pass

def decifrar_RSA(d):
  pass

