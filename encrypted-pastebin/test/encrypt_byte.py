import sys
from random import randrange
from Crypto.Cipher import AES

class PaddingException(Exception):
    pass


staticKey = bytes([0] * 16)


def encrypt(iv, data):
    cipher = AES.new(staticKey, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(data)
    return encrypted

def decrypt(iv, data):
    cipher = AES.new(staticKey, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(data)
    return decrypted


def unpad(data):
    ldata = memoryview(data)
    pd_bytes = ldata[-1]

    # los datos son mas largos que el pad.
    if len(data) < pd_bytes:
        raise PaddingException()

    # chequeo que todos los bytes sean iguales.
    pad_bytes = ldata[-pd_bytes:]
    b = pad_bytes[0]
    for i in pad_bytes:
        if b != i:
            raise PaddingException()

    return bytes(ldata[:-pd_bytes])

def pad(data):
    pad_byte = 16 - (len(data) % 16)
    return data + bytes(pad_byte for i in range(pad_byte))

def encrypt_paddle_oracle(c2:bytes, plaintext):
    iv = bytearray([randrange(255) for _ in range(16)])
    p2p = [0] * 16
    c1 = [0] * 16

    for i in range(15,-1,-1):
        for b in range(256):
            print(f'probando byte {b}')
            iv[i] = b
            data = decrypt(bytes(iv),c2)
            try:
                ud = unpad(data)
                pad = 16 - i
                p2p[i] = iv[i] ^ pad
                c1[i] = p2p[i] ^ plaintext[i]
                print(iv.hex())
                print(c2.hex())

                pad = pad + 1
                for a in range(i,16):
                    iv[a] = p2p[a] ^ pad

                break

            except PaddingException:
                pass

    return bytes(c1)

def obtener_bloques(data:bytes):
    bloques = []
    for i in range(0, len(data), 16):
        bloques.append(data[i:i+16])
    return bloques

if __name__ == '__main__':
    iv = bytes(16)
    d = pad(b'{"id":"1", "key":"1234567891234567"}')
    e = encrypt(iv,d)
    print(e.hex())
    data = decrypt(iv,e)
    print(data.hex())
    print(data)

    plaintext = pad(b'{"id":"123", "key":"1231029312903821903293130209312", "hackme":"yeababy"}')
    plains = obtener_bloques(plaintext)
    print(plains)

    blocks = []
    #c2 = e[-16:]
    c2 = bytes([randrange(255) for _ in range(16)])
    blocks.append(c2)

    plains.reverse()
    for plain in plains:
        c1 = encrypt_paddle_oracle(c2,plain)
        blocks.append(c1)
        c2 = c1

    datae = b''
    for b in blocks:
        datae = b + datae

    iv = datae[:16]
    datas = datae[16:]

    data = decrypt(iv,datas)
    print(len(data))
    print(data.hex())
    print(data)
    
    