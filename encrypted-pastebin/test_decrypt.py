import base64
import binascii
from Crypto.Cipher import AES


with open('hash.bin','rb') as f:
    hash_ = f.read()

print(len(hash_))

iv = base64.b64decode('sbioNf5FsbHI8568PkXC2w==')
static_key = bytes([0] * 15 + [1])

cipher = AES.new(static_key, AES.MODE_CBC, iv)
decripted = cipher.decrypt(hash_)
print(binascii.hexlify(decripted))
print(decripted)
print(decripted.decode('utf8'))