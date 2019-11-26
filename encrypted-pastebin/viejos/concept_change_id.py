import base64
import binascii
from Crypto.Cipher import AES

data = "{\"flag\": \"^FLAG^871316352eb20f698291dc4d4c5678240c03f8b22d4e98114b04a32da6bed1bf$FLAG$\", \"id\": \"2\", \"key\": \"sbioNf5FsbHI8568PkXC2w~~\"}"
extradata = binascii.unhexlify('0a0a0a0a0a0a0a0a0a0a')
lastblock = binascii.unhexlify('00000000000000000000000000000001')
#static_key = base64.b64decode('sbioNf5FsbHI8568PkXC2w==')
iv = bytes([0] * 15 + [1])
static_key = bytes([0] * 16)

bl = (int(len(data)/16) + 1) * 16
blocks = bytes(data.encode('utf8')) + extradata 
lblocks = list(blocks)

print(len(lastblock))

import common
print('sin padding')
print(binascii.hexlify(common.unpad(blocks)))


cipher = AES.new(static_key, AES.MODE_CBC, iv)
cripted = cipher.encrypt(blocks)
print(binascii.hexlify(cripted))


with open('hash.bin','rb') as f:
    hash_ = f.read()

print(binascii.hexlify(hash_))

"""

print(lblocks[96])
print(chr(lblocks[96]))

lcripted = list(cripted)

liv2 = [0] * 16
liv2[1] = lblocks[1] ^ 0 ^ 50
iv2 = bytes(liv2)
cipher2 = AES.new(static_key, AES.MODE_CBC, iv2)
decripted = cipher2.decrypt(bytes(lcripted))
print(binascii.hexlify(decripted))
print(decripted)
print(decripted.decode('utf8'))

"""