from RSA import *
import hashlib
import base64


def decifrar_assinatura(assinaturaBase64, chave_publica):
    n, e = chave_publica
    
    cifra_assinatura = int.from_bytes(base64.b64decode(assinaturaBase64.encode()), byteorder='big')    
    hash_assinatura_decifrada = pow(cifra_assinatura, e, n)
    
    return hash_assinatura_decifrada


def verificar_assinatura(documento_assinado, chave_publica, assinaturaBase64):
    n, e = chave_publica
    
    cifra_assinatura = int.from_bytes(base64.b64decode(assinaturaBase64.encode()), byteorder='big')
    
    hash_mensagem_decifrada = pow(cifra_assinatura, e, n)
    hash_documento_original = calcular_hash_sha3(documento_assinado)
    
    if hash_mensagem_decifrada == int.from_bytes(hash_documento_original, byteorder='big'):
        return True
    else:
        return False


def assinar_mensagem(mensagem, chave_privada):
    n, d = chave_privada
    
    hash_mensagem = calcular_hash_sha3(mensagem) #calcula o hash
    
    cifra_assinatura = pow(int.from_bytes(hash_mensagem, byteorder='big'), d, n) #decifraa com RSA
    
    #formata resultad em base64
    assinaturaBase64 = base64.b64encode(cifra_assinatura.to_bytes((cifra_assinatura.bit_length() + 7) // 8, byteorder='big')).decode()
    
    return assinaturaBase64


def calcular_hash_sha3(mensagem):
    hash_obj = hashlib.sha3_256(mensagem.encode())
    hash_resultado = hash_obj.digest()
    return hash_resultado