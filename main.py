from assinatura import *
from RSA import *

chaves_privadas, chaves_publicas = generate_keys()
texto = "outro teste"


texto_pad = aplicar_oaep(texto, chaves_publicas)

cifra = hex(cifrar_RSA(texto_pad, chaves_publicas))
print(cifra)
texto_decifrado = decifrar_RSA(int(cifra,16), chaves_privadas)
texto_sem_pad = remover_oaep(texto_decifrado, chaves_privadas)
print('\n', texto_sem_pad)




msg_original = texto #original

#assina documento
assinaturaBase64 = assinar_mensagem(msg_original, chaves_privadas)

#msg_original = 'hello' #modificada teste


if verificar_assinatura(msg_original, chaves_publicas, assinaturaBase64): #checar a autenticidade da assinatura
    print("\nAssinatura válida.")
else:
    print("\nAssinatura inválida.")

