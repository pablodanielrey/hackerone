
import binascii

with open('hash.bin','rb') as f:
    hash_ = f.read()

print(binascii.hexlify(hash_))

import common
import base64

print(base64.b64encode(hash_))

print(common.b64e(hash_))