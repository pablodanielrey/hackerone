import binascii
import utils
"""
    contenido del hash decodificado:
    {"flag": "^FLAG^871316352eb20f698291dc4d4c5678240c03f8b22d4e98114b04a32da6bed1bf$FLAG$", "id": "2", "key": "sbioNf5FsbHI8568PkXC2w~~"}

    y de extra data:

    extradata = binascii.unhexlify('0a0a0a0a0a0a0a0a0a0a00000000000000000000000000000001')
"""

with open('hash.bin','rb') as f:
    hash_ = f.read()

lhash = list(hash_)

original_data = binascii.unhexlify('7b22666c6167223a20225e464c41475e3837313331363335326562323066363938323931646334643463353637383234306330336638623232643465393831313462303461333264613662656431626624464c414724222c20226964223a202232222c20226b6579223a20227362696f4e6635467362484938353638506b584332777e7e227d0a0a0a0a0a0a0a0a0a0a00000000000000000000000000000001')
lod = list(original_data)

print(len(hash_))
print(len(original_data))

print('hash original ' + binascii.hexlify(hash_).decode('utf8'))

url = 'http://35.227.24.107/b6b38fea92/'

lhash[-2] = 0x2
dhash = bytes(lhash)

print('hash a enviar ' + binascii.hexlify(dhash).decode('utf8'))

(t,b) = utils.decript_data(url, dhash)
print(t)
print(b)
