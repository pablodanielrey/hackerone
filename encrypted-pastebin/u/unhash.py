
import common
import sys
import binascii

s = sys.argv[1]
print(len(s))
print(s)


d = common.b64d(s)
print(len(d))
print(binascii.hexlify(d))
print(d)
try:
    print(d.decode('utf8'))
except Exception as e:
    pass