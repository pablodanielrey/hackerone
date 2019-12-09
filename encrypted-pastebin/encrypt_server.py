import sys
import requests
from random import randrange
from Crypto.Cipher import AES

from u.common import b64e, b64d
from u.utils import encrypt_data

class PaddingException(Exception):
    pass


url = 'http://34.74.105.127/085047b1af/'

def decrypt(data:memoryview) -> bytes:
    global url
    de = b64e(data)
    r = requests.get(f'{url}?post={de}',  proxies={'http':'http://127.0.0.1:8080'}, allow_redirects=False)
    #r = requests.get(f'{url}?post={de}',  allow_redirects=False)
    return r.text

def check_padding_error(d) -> bool:
    return type(d) is str and 'PaddingException' in d


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
    w = memoryview(iv + c2)
    iv = w[:16]
    p2p = [0] * 16
    c1 = [0] * 16

    for i in range(15,-1,-1):
        print(f'probando pos {i}')
        for b in range(256):
            iv[i] = b
            data = decrypt(w)
            if check_padding_error(data):
                continue

            print(f'byte encontrado {b}')
            pad = 16 - i
            p2p[i] = iv[i] ^ pad
            c1[i] = p2p[i] ^ plaintext[i]
            print(iv.hex())
            print(c2.hex())

            pad = pad + 1
            for a in range(i,16):
                iv[a] = p2p[a] ^ pad

            break

    return bytes(c1)

def obtener_bloques(data:bytes):
    bloques = []
    for i in range(0, len(data), 16):
        bloques.append(data[i:i+16])
    return bloques

if __name__ == '__main__':
   
    plaintext = pad(b'{"id":"1", "key":"1231029312903821903293130209312"}')
    plains = obtener_bloques(plaintext)
    print(plains)

    blocks = []
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

    print(len(datae))
    print(datae.hex())
    print(datae)
    try:
        print(datae.decode('utf8'))
    except Exception:
        pass