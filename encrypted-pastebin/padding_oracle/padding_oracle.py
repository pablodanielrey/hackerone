

def padding_oracle(c1:bytes, c2:bytes, decrypt, check_padding_error) -> bytes:
    w = memoryview(bytearray(16) + bytearray(c2))
    c1p = w[:16]
    des = [0] * 16 
    for i in range(15,-1,-1):
        for b in range(256):
            c1p[i] = b
            p_ = decrypt(w)
            if check_padding_error(p_):
                continue
            pad = 16 - i
            des[i] = pad ^ c1[i] ^ c1p[i]
            # ajusto el pad para el proximo byte a descubrir.
            pad = pad + 1
            for a in range(i,16):
                c1p[a] = pad ^ des[a] ^ c1[a]

            print(f'byte {b} encontrado para posición {i}')
            break
        else:
            print('no se encontro nada!!! esto es un error')
    return bytes(des)

