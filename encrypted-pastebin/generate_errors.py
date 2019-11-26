import requests
import common
import binascii


import utils

#for p in range(1,4):


data = [0x41 for a in range(0,34)]
bdata = bytes(data)
p = requests.post("http://35.227.24.107/51980f8ea3/", data={ 'title':'', 'body':bdata }, proxies={'http':'http://127.0.0.1:8080'}, allow_redirects=False)
print(p.text)

hash_ = utils.extract_hash(p.text)
dhash = common.b64d(hash_)
lhash = list(dhash)
tamano = len(dhash)

print('hash:')
utils.print_hash(dhash)

inicio = tamano - ((16 * 2) + 1)
fin = tamano - 16
lblock = lhash[inicio:fin]


solucion = {}

for h in range(15,0,-1):
    for i in range(0,256):
        lblock[h] = i
        rhash = lhash[:inicio] + lblock + lhash[fin:]
        bhash = bytes(rhash)
        shash = common.b64e(bhash)
        print(f'{h},{i}')
        text = utils.test_hash(shash)
        if 'PaddingException' not in text and 'Error' not in text:
            utils.print_hash(bhash)
            print(text)
            print(i)
            solucion[h] = i
            print(solucion)
            break

print(solucion)


