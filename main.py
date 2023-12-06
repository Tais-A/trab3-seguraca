from assinatura import *
from RSA import *

print("========= Gerando Chaves =========")
chaves_privadas, chaves_publicas = generate_keys()


print("\n\n========= Lendo Arquivo =========")
with open("./arquivo.txt", "rb") as arquivo:
    data = arquivo.read()
    print("Arquivo lido: ", data)
    data_base64 = base64.b16encode(data)
    mensagem = str(data_base64,"ascii").upper()


    
print("\n\n========= Cifra RSA/OAEP =========")
texto_pad = aplicar_oaep(mensagem, chaves_publicas)
cifra = hex(cifrar_RSA(texto_pad, chaves_publicas))
print(cifra)

print("\n\n========= Texto Decifrado =========")
texto_decifrado = decifrar_RSA(int(cifra,16), chaves_privadas)
texto_sem_pad = remover_oaep(texto_decifrado, chaves_privadas)
print("Arquivo em base64: ", texto_sem_pad)
print("Conteudo: ", base64.b16decode(texto_sem_pad))


print("\n\n========= Verificando Assinatura =========")
msg_original = mensagem #original

#assina documento
assinaturaBase64 = assinar_mensagem(msg_original, chaves_privadas)

#msg_original = 'hello' #modificada teste


if verificar_assinatura(msg_original, chaves_publicas, assinaturaBase64): #checar a autenticidade da assinatura
    print("\nAssinatura válida.")
else:
    print("\nAssinatura inválida.")

