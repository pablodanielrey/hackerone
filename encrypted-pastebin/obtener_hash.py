import sys
import json
import binascii
import u.utils
import u.common

url = sys.argv[1]
hash_file = 'hash.json'
try:
    hash_file = sys.argv[2]
except Exception as e:
    pass

index = 0
try:
    index = sys.argv[3]
except Exception as e:
    pass

print(f"Obteniendo hash desde : {url} y almacenando en : {hash_file}")

title = 't'
body = 'b'

hash_ = u.utils.encript_data(url, title, body)

hash_data = {
    'url': url,
    'data_title': title,
    'data_body': body,
    'hash_index': index,
    'hash_get': u.common.b64e(hash_),
    'hash': binascii.hexlify(hash_).decode('utf8')
}

print(f"Datos del Hash : {hash_data}")

with open(hash_file,'w') as f:
    f.write(json.dumps(hash_data))

