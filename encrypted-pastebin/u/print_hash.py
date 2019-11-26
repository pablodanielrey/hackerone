
import sys
import binascii
import common

a = sys.argv[1]
with open(a, 'rb') as f:
    hash_ = f.read()

print(binascii.hexlify(hash_))
print(common.b64e(hash_).encode('utf8'))