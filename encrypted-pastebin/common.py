import base64
import json
from Crypto.Cipher import AES

class PaddingException(Exception):
    pass

b64d = lambda x: base64.decodestring(x.replace('~', '=').replace('!', '/').replace('-', '+').encode('utf-8'))

def unpad(data):
    ldata = list(data)
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

"""
def decryptLink(data) -> bytes:
    data = b64d(data)
    cipher = AES.new(staticKey, AES.MODE_CBC, iv)
    ret = unpad(cipher.decrypt(data))
    return ret
"""

b64e = lambda x: base64.b64encode(x).decode('utf8').replace('=','~').replace('/','!').replace('+','-')


def desencriptar(key,data):
    cipher = AES.new(key, AES.MODE_ECB)
    dec = cipher.decrypt(data)
    return dec
