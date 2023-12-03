import math
import hashlib
import sys
import binascii
import os


def HexstringToCharacters(hexstr):
    if len(hexstr) % 2 == 1:
        hexstr = '0' + hexstr
    return bytes.fromhex(hexstr).decode('latin-1')


def MGF(hash_semente, k):
    dchar = HexstringToCharacters(hash_semente)

    contador = int(math.floor(k * 1.0 / 20))
    data = dchar + '\x00\x00\x00\x00'
    saida = int(hashlib.sha1(data.encode()).hexdigest(), 16)

    for i in range(1, contador + 1):
        data = dchar + '\x00\x00\x00' + chr(i)
        data = int(hashlib.sha1(data.encode()).hexdigest(), 16)
        saida = (saida << 160) | data
    saida >>= ((contador + 1) * 160 - k * 8)
    return hex(saida)[2: int(2 * k + 2)]



def aplicar_oaep(mensagem, chaves_publicas):
    n,e = chaves_publicas
    tamanho_mensagem = len(mensagem)
    mensagem_hex = mensagem.encode().hex()
  
    
    random_bytes = os.urandom(20)
    random_hash_r = hashlib.sha1(random_bytes).hexdigest()
    hash_r = int(random_hash_r,16)

    tamanho_chave = int(n.bit_length() / 8)
    tamanho_hash_r = int(hash_r.bit_length() / 8)
    tamanho_preenchimento = int(tamanho_chave - 2 * tamanho_hash_r - tamanho_mensagem - 2)


    if tamanho_preenchimento < 0:
        raise ValueError("Mensagem muito longa")
    else:
        ps = '00' * tamanho_preenchimento


    hash_l = hashlib.sha1().hexdigest()
    tamanho_hash_l = int(len(hash_l) / 2)

    pad = int(hash_l + ps + '01' + mensagem_hex, 16)

    hash_r_hex = hex(hash_r)[2:]
    k = tamanho_hash_r + tamanho_preenchimento + tamanho_mensagem + 1

  
    db = int(MGF( hash_r_hex, k), 16) ^ pad
    db_hex = hex(db)[2:]
    mascara_db = int(MGF(db_hex, tamanho_hash_r), 16) ^ hash_r
    mascara_db_hex = hex(mascara_db)[2:]
    mensagem_pad = '00' + mascara_db_hex + db_hex

    return int(mensagem_pad,16)


def remover_oaep(cifra, chave_privada):
    n,d = chave_privada
    cifra_hex = hex(cifra)[2:]
    hash_l = hashlib.sha1().hexdigest()

    tamanho_cifra = len(cifra_hex)
    tamanho_chave = int(n.bit_length()/8)
    tamanho_hash = int(len(hash_l)/2)


    tamanho_preenchimento_e_mensagem = int(tamanho_cifra - tamanho_chave - 2 * tamanho_hash)
    k = tamanho_hash + tamanho_preenchimento_e_mensagem + 1

    db = (pow(2, 8 * k) - 1) & cifra
    db_hex = (hex(db)[2:])
    mascara_db_hex = cifra_hex[:-(len(db_hex))]
    mascara_db = int(mascara_db_hex,16)

    hash_r = mascara_db ^ int(MGF(db_hex, tamanho_hash), 16)
    hash_r_hex = hex(hash_r)[2:]

    pad = db ^ int(MGF( hash_r_hex, k), 16) 

    pad_hex = hex(pad)[2:]

    mensagem_bytes =  bytes.fromhex(pad_hex)
    return(mensagem_bytes.decode('latin-1'))

    preenchimento_e_mensagem = pad_hex[len(hash_l):]
    # for i in range(len(preenchimento_e_mensagem)):
    #     if preenchimento_e_mensagem[i] != '0':
    #         mensagem = preenchimento_e_mensagem[i+1:]
        
            

    # print('mensagem ', mensagem)
    # mensagem_bytes =  bytes.fromhex(mensagem)
    # print(mensagem_bytes)

    # return mensagem_bytes.decode('utf-8')


