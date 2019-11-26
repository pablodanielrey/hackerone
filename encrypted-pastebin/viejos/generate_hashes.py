import base64
import sys
import requests
import re
import binascii
import json

import common


rhash = re.compile(r"href=\"\?post=(.*?)\">")

title = "1"
body="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

hashes = []

for i in range(1,4):
    p = requests.post("http://35.227.24.107/51980f8ea3/", data={
        'title':title,
        'body':body
    }, proxies={'http':'http://127.0.0.1:8080'}, allow_redirects=False)
    if not p.ok:
        print('error generando hash : ')
        print(p.text)
        print(p.status_code)
        continue
    html = p.text
    m = rhash.search(html)
    if not m:
        print('algo salió mal extrayendo el hash')
        continue
    hash_ = m.group(1)
    hashes.append(hash_)

print(hashes)

jhashes = {}

for i,h in enumerate(hashes):
    b = common.b64d(h)
    h_ = binascii.hexlify(b).decode('utf8')
    #h__ = common.b64e(b)
    k_ = b[:16]
    e_ = b[16:]
    d_ = binascii.hexlify(common.desencriptar(k_,e_)).decode('utf8')
    jhashes[f'hash_{i}'] = {
        'hash': h,
        'hash_len': len(h),
        'hex': h_,
        'hex_len': len(h_),
        #'re_hash': h__,
        #'re_hash_len': len(h__),
        'decoded_key': binascii.hexlify(k_).decode('utf8'),
        'decoded_key_len': len(k_),
        'encoded_data': binascii.hexlify(e_).decode('utf8'),
        'encoded_data_len': len(e_),
        'decoded_bytes':d_,
        'decoded_bytes_len':len(d_)
    }


with open(f'hashes.json','w') as f:
    f.write(json.dumps(jhashes))
    
