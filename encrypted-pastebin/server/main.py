import json
import binascii
from Crypto.Cipher import AES

import u.common


class PaddingException(Exception):
    pass

staticKey = bytes([0] * 16)

"""
    Esta parte de código ayuda a encriptar un dato válido de ejemplo.
    infiero que hace este proceso desde los errores reportados y análisis de los datos desencriptados.
    el iv deberían ser los últimos 16 bytes agregados al hash encriptado
"""

def process_get():
    data = '{"flag": "^FLAG^871316352eb20f698291dc4d4c5678240c03f8b22d4e98114b04a32da6bed1bf$FLAG$", "id": "10", "key": "n!JJNaHmDk4VlmeNfNuuNA~~"}'
    encoded = data.encode('utf8')

    print(encoded)
    print(binascii.hexlify(encoded))
    print(len(encoded))

    padded = pad(encoded)

    print(padded)
    print(binascii.hexlify(padded))
    print(len(padded))

    hash_ = encrypt(padded)

    print(hash_)
    print(binascii.hexlify(hash_))
    print(len(hash_))

    bhash = u.common.b64e(hash_)
    return bhash

def encrypt(data):
    iv = bytes([0x20] * 16)
    cipher = AES.new(staticKey, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(data)
    return encrypted + iv

def pad(data):
    if len(data) % 16 == 0:
        """ asumo que  en esta condición crea otro bloque completo de padding porque siempre hace unpad cuando procesa la solicitud """
        return data + bytes([16] * 16)
    padd_bytes = (((int(len(data) / 16)) + 1) * 16) - len(data)
    return data + bytes([padd_bytes] * padd_bytes)


"""
    Esta parte de código sería la que corre en el servidor para procesar cada hash enviado.
"""

def process_request(postCt):
    post = json.loads(decryptLink(postCt).decode('utf8'))
    # ahora se accede a los datos del post para retornar.
    return post

def decryptLink(data):
    data = u.common.b64d(data)
    iv = data[-16:]
    payload = data[:-16]
    cipher = AES.new(staticKey, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(payload))

def unpad(data):
    padding = data[-1]
    pad_bytes = data[-padding:]
    for b in pad_bytes:
        if b != padding:
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