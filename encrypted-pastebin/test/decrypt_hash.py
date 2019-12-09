import sys
import base64
from random import randrange
from Crypto.Cipher import AES

"""
    el cuerpo del post = 1
"""

body = 'YEEL3Dw3Fz!FcMdod3w97J2m22RqdkhjjVZzXBLNiJhXgmQCM7CT2YSbQT5P0Btu5UFuT4oT!-MY!no71DCpVWW0QvOAXQW-GOnXzqGqMlC8SOBuKmy9580l5SMzXf1t'

b64d = lambda x: base64.decodestring(x.replace('~', '=').replace('!', '/').replace('-', '+').encode('utf-8'))


class PaddingException(Exception):
    pass

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
    

def decrypt(iv, data, key):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(data)
    return decrypted

if __name__ == '__main__':

    print(b64d(body).hex())


    key = bytes([0] * 16)
    iv = body[:16]
    data = body[16:]

    for k in (x for x in range(0, 2**128)):
        key = k.to_bytes(16,'little')
        print(f'testing {k} --> {key.hex()}')
        d = decrypt(iv, data, key)
        try:
            un = unpad(d)
            #print('DESENCRIPTADO!!!:')
            #print(un.hex())
            #print(un)
            try:
                print(un.decode('utf8'))
                sys.exit(0)
            except Exception:
                pass
        except PaddingException:
            pass



