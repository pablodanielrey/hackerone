

def padding_oracle(c1:bytes, c2:bytes, decrypt, check_padding_error) -> bytes:
    w = memoryview(bytearray(16) + bytearray(c2))
    c1p = w[:16]
    des = [0] * 16 
    for i in range(15,-1,-1):
        bytes_to_test = [bb for bb in range(c1[i])] + [bb for bb in range(c1[i] + 1,256)] + [c1[i]]
        for b in bytes_to_test:
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

def calculate_new_iv(iv:bytes, decrypted:bytes, caracteres:bytes) -> bytes:
    """
        genera un nuevo iv para dejar en el bloque deseado los caracteres
        iv --> iv actual
        decrypted --> caracteres resultantes desencriptados
        caracteres --> caracteres que se quiere como resultado final
    """
    print('calculando nuevo IV')
    nuevo_iv = [0] * 16
    for i in range(16):
        nuevo_iv[i] = iv[i] ^ decrypted[i] ^ caracteres[i]
        print(f'{nuevo_iv[i]:02x} <-- {iv[i]:02x} ^ {decrypted[i]:02x} ^ {caracteres[i]:02x}')
    return bytes(nuevo_iv)
