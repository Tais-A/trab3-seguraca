from MillerRabin import gerar_primo
import random
import base64
from OAEP import aplicar_oaep, remover_oaep

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
  print(phi)
  d = None
  while not d:
    e = expoente_publico(tamanho_chave, phi)
    d = inverso_multiplicativo(e, phi)
  chaves_privadas = [n,d]
  chaves_publicas = [n,e]
  print ()
  print(f"chaves públicas: \n\n n => {n} \n\n e => {e}\n")
  print(f"chaves privadas: \n\n p => {p} \n\n q => {q} \n\n d => {d}\n")
  return ([chaves_privadas,chaves_publicas])


def exponenciacao_modular(base, expoente, modulo):
    resultado = 1
    base = base % modulo
    while expoente > 0:
        if expoente % 2 == 1:
           resultado = (resultado * base) % modulo
        expoente = expoente // 2
        base = (base * base) % modulo
    return resultado


def cifrar_RSA(m,chave):
  n, e = chave
  return pow(m, e, n)


def decifrar_RSA(c,chave):
  n, d = chave
  return pow(c, d, n)

e=315072639181787062204879454268468717029642581191469403652027548364984167814759524621854969639659481272332748985472247024008338394338379454582162372873401251477240923315720519690353827732131542020163093964119602676188044560952180629837337921662014916892312453151226720930963823198370569743924630809761423407249

n=36070617079629761940943401571285382969248094431810409195433940624707219784271076295597103405659542411977910462627438163696941448720415195204679709153573594929499522036624714864448145899888648089737689459387626700600649099053594510133696196530416886546980731478383054325692675146833175660058380327353443158650253295915898534902049922845957987570040444253048600261128759091507718655229880623876093703613332110303754666551322615438112211985739796376732785067256882804746486871470507831303513180276218928528396913153657831498938814423049345790060735396005887983996998928952231251203426444926158455910178040023747478117339

d=13258304597964970965364186771570584341377061587387470237974589194545145686736908586230440005799253124131101785473377391584112524059875465333382534325146282985314467260694182326188057456712131461291811749800693160132288390664151731860346956836895834225889450167983013282204869644994019112466838703997890107978501748721948606855068070273110743552323422012620855710133798933171902256971310034087657847938154659635367328311280800065913284756122011867205863924802447392466966972430565851089127495068477578834605296545593531676308090683416363326503039794227378726144105378625587188018838822794056876497801768187758804944657


texto = "outro teste"
chaves_privadas = [n,d]
chaves_publicas = [n,e]



texto_pad = aplicar_oaep(texto, chaves_publicas)

cifra = hex(cifrar_RSA(texto_pad, chaves_publicas))
print(cifra)
texto_decifrado = decifrar_RSA(int(cifra,16), chaves_privadas)
texto_sem_pad = remover_oaep(texto_decifrado, chaves_privadas)
print(texto_sem_pad)
