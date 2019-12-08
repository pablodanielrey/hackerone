"""
    prueba de concepto para ver si el algoritmo fuciona contra AES CBC mode.
    y poder codificar algo en modo binario sin preocupación por la decoficiación de utf.
"""

from random import randrange
from Crypto.Cipher import AES


class PaddingException(Exception):
    pass

def pad(data : bytes) -> bytes:
    pad_byte = 16 - (len(data) % 16)
    return data + bytes(pad_byte for i in range(pad_byte))

def unpad(data : bytes) -> bytes:
    if not data or len(data) % 16:
        raise PaddingException()
    padding = data[-1]
    if padding > 16:
        raise PaddingException()
    pad_bytes = data[-padding:]
    if not all(i == padding for i in pad_bytes):
        raise PaddingException()
    return data[:-padding]

def print_block(b : bytes):
    print('-'*16)
    print(b.hex())
    print('-'*16)

staticKey = bytes([randrange(255) for _ in range(16)])
iv = bytes([randrange(255) for _ in range(16)])

def encrypt(data : bytes) -> bytes:
    cipher = AES.new(staticKey, AES.MODE_CBC, iv)
    return cipher.encrypt(data)

def decrypt(data: bytes) -> bytes:
    cipher = AES.new(staticKey, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(data))

