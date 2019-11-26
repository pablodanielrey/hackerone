
import Crypto
from Crypto.Cipher import AES
import binascii
import base64

ckey = 'sbioNf5FsbHI8568PkXC2w~~'
bkey = ckey.replace('~','=').replace('!','/').replace('-','+')
key = base64.b64decode(bkey)

with open('hash.bin','rb') as f:
    hash_ = f.read()

print(binascii.hexlify(hash_))

iv = bytes(list(hash_)[:16])
cipher = AES.new(key,AES.MODE_CBC,iv)
d = cipher.decrypt(hash_)
print(binascii.hexlify(d))
print(d.decode('utf8'))
