import base64
import sys
import requests
import re
import binascii
import json

import common

rhash = re.compile(r"href=\"\?post=(.*?)\">")

title = "1"
body="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

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

for i,h in enumerate(hashes):
    b = common.b64d(h)
    with open(f'h{i}.bin','bw') as f:
        f.write(b)