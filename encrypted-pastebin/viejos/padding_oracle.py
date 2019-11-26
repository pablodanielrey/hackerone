"""
    Dados P y C, P siendo el segundo bloque a descubrir. y C siendo el primer bloque cifrado.
    para el primer byte, tenemos que :

    P_2[15] = C_1[15] (+) C_1`[15] (+) 0x01

    para el segundo byte tenemos que calcular primero un nuevo valor para C_1`[15] para que resuelva a 0x02
    asi cuando testeamos el anteúltimo byte sabemos que el último siempre es 0x02 cumpliendo PCKS#7

    new_C_1`[15] = P_2[15] (+) C_1[15] (+) 0x02

"""


import binascii
import common
import utils
import sys

def print_decoded_bytes(decoded_bytes):
    try:
        print(decoded_bytes)
        db = bytes(decoded_bytes)
        print(binascii.hexlify(db))
        print(db.decode('utf8'))    
    except Exception as e:
        print(f'error impirmirneod {e}')

url = 'http://35.227.24.107/b6b38fea92/'

try:
    with open('hash.bin','rb') as f:
        hash_ = f.read()
except Exception as e:
    hash_ = utils.encript_data(url, 'titulo', 'cuerpo')
    with open('hash.bin','wb') as f:
        f.write(hash_)

lhash = list(hash_)

# variables que delimitan el bloque a manipular
t = len(hash_)
tam_bloque = 16
bloques = int(t/tam_bloque)
b = bloques - 2

decoded_bytes = [0] * len(hash_) 

print(f'cantidad de bloques : {bloques}')

bloque_inicial = 0
try:
    bloque_inicial = int(sys.argv[1])
except Exception as e:
    pass

print(f'iniciando procesamiento por el bloque {bloque_inicial}')

for b in range(bloque_inicial,bloques,1):

    i = b * tam_bloque
    f = (b * tam_bloque) + tam_bloque

    block = lhash[i:f]
    dhash_ = lhash[:i] + block + lhash[f:f+16]

    original_bytes = [0] * 16

    encontrado = True
    for position_in_block in range(15,-1,-1):
        if not encontrado:
            break
        encontrado = False
        original_bytes[position_in_block] = block[position_in_block]
        bytes_to_test = [c for c in range(0,original_bytes[position_in_block])] + [c for c in range(original_bytes[position_in_block] + 1, 256)] + [original_bytes[position_in_block]]
        for c in bytes_to_test:
            if encontrado:
                break
            block[position_in_block] = c
            dhash_ = bytes(lhash[:i] + block + lhash[f:f+16])
            #dhash_ = bytes(block + lhash[f:f+16])
            #utils.print_hash(dhash_)
            try:
                (t, d) = utils.decript_data(url, dhash_)
                padding = (16 - position_in_block)
                decoded_bytes[(b * 16) + position_in_block] = block[position_in_block] ^ original_bytes[position_in_block] ^ padding
                for pad in range(position_in_block,16):
                    block[pad] = decoded_bytes[(b * 16) + pad] ^ original_bytes[pad] ^ (padding + 1)
                print(f'Solución block {b} pos : {position_in_block}')
                print_decoded_bytes(decoded_bytes)
                encontrado = True
            except Exception as e:
                pass

print_decoded_bytes(decoded_bytes)
