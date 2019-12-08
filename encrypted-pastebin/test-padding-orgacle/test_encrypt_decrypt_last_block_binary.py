from random import randrange
from enc import encrypt, pad, decrypt, print_block, PaddingException

def padding_oracle(c1:bytes, c2:bytes) -> bytes:
    w = memoryview(bytearray(16) + bytearray(c2))
    c1p = w[:16]
    des = [0] * 16 

    print('usando bloque para desencriptar')
    print_block(w)

    for i in range(15,-1,-1):
        print('-'*16)
        print(f'indice : {i}')

        for b in range(256):
            c1p[i] = b
            try:
                p_ = decrypt(bytes(w))
                print_block(w)
                print(f'datos desencriptados : {p_.hex()}')
                print(f'encontrado : {b}')
                print(f'bloque encontrado : {w.hex()}')
                pad = 16 - i
                des[i] = pad ^ c1[i] ^ c1p[i]
                print(f'valor desencriptado : {des[i]:02x}')
                # ajusto el pad para el proximo byte a descubrir.
                pad = pad + 1
                for a in range(i,16):
                    c1p[a] = pad ^ des[a] ^ c1[a]
                break

            except PaddingException:
                pass
        else:
            print('no se encontro nada!!! esto es un error')
    return bytes(des)


blocks = 5
extra = 12

block_to_encrypt = pad(bytes([randrange(255) for _ in range((16*blocks) + extra)]))
h_ = encrypt(block_to_encrypt)
hash_ = memoryview(h_)

print(f'bloque a encriptar : {block_to_encrypt.hex()}')
print(f'bloque encriptado  : {h_.hex()}')

decrypted = None

for b in range(blocks):
    i = b * 16
    f = i + 16
    c1 = hash_[i:f]
    c2 = hash_[f:f+16]
    des = padding_oracle(c1,c2)
    if not decrypted:
        decrypted = des
    else:
        decrypted = decrypted + des

print(f'bloque original      : {block_to_encrypt[16:].hex()}')
print(f'bloque desencriptado : {decrypted.hex()}')