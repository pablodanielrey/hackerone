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

# queremos que el  id:"2" se transforme en id:"1"
# para esto sabemos que es el byte 96 del hash, y tenemos el byte original, por lo que
# podemos hacer un XOR para modificar el valor:
# byte_original (+) byte_cifrado (+) byte_deseado

data = "{\"flag\": \"^FLAG^871316352eb20f698291dc4d4c5678240c03f8b22d4e98114b04a32da6bed1bf$FLAG$\", \"id\": \"2\", \"key\": \"sbioNf5FsbHI8568PkXC2w~~\"}"
ldata = list(data.encode('utf8'))

print(binascii.hexlify(data.encode('utf8')))


lhash = list(hash_)
print(binascii.hexlify(hash_))



url = 'http://35.227.24.107/b6b38fea92/'

cindex = 96-16
pindex = 96

#byte_reemplazo = hash_[index] ^ ldata[index] ^ 0
byte_reemplazo = hash_[cindex] ^ ldata[pindex] ^ 3
print(byte_reemplazo)
lhash[cindex] = byte_reemplazo
dhash = bytes(lhash)
print(binascii.hexlify(dhash))

(t,b) = utils.decript_data(url, dhash)
print(t)
print(b)
