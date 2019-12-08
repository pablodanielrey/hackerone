import traceback
import json
import binascii
from Crypto.Cipher import AES

import u.common


class PaddingException(Exception):
    pass

staticKey = bytes([0] * 16)
iv = bytes([2] * 16)

"""
    Esta parte de código ayuda a encriptar un dato válido de ejemplo.
    infiero que hace este proceso desde los errores reportados y análisis de los datos desencriptados.
    el iv, por el comportamiento de error, deberían ser los últimos 16 bytes agregados al hash encriptado
"""

def process_get():
    data = '{"flag": "^FLAG^871316352eb20f698291dc4d4c5678240c03f8b22d4e98114b04a32da6bed1bf$FLAG$", "id": "10", "key": "n!JJNaHmDk4VlmeNfNuuNA~~"}'
    encoded = data.encode('utf8')
    padded = pad(encoded)
    hash_ = encrypt(padded)
    bhash = u.common.b64e(hash_)
    return bhash

def encrypt(data):
    #iv = bytes([0x20] * 16)
    cipher = AES.new(staticKey, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(data)
    return iv + encrypted
    #return encrypted


def pad(data):
    pad_byte = 16 - (len(data) % 16)
    return data + bytes(pad_byte for i in range(pad_byte))

"""
    Esta parte de código sería la que corre en el servidor para procesar cada hash enviado.
"""

def process_request(postCt):
    try:
        post = json.loads(decryptLink(postCt).decode('utf8'))
        # ahora se accede a los datos del post para retornar.
        return post
    except Exception:
        return traceback.format_exc()
        #return str(e.__class__)

def decryptLink(data):
    ddata = u.common.b64d(data)
    iv = ddata[:16]
    payload = ddata[16:]
    #payload = ddata
    cipher = AES.new(staticKey, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(payload))


def unpad(data):
    if not data or len(data) % 16:
        raise PaddingException()

    padding = data[-1]
    if padding > 16:
        raise PaddingException()

    pad_bytes = data[-padding:]
    if not all(i == padding for i in pad_bytes):
        raise PaddingException()

    return data[:-padding]

"""
inferido a partir de los errores reportados
def _d():
46 - data = b64d(data)
47 - ??? iv = data[-16:]
48 - cipher = AES.new(staticKey, AES.MODE_CBC, iv)
49 - return unpad(cipher.decrypt(data))    
"""