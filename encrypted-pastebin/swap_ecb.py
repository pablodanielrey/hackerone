import base64
import sys
import requests
import re
import binascii
import json

import common

rhash = re.compile(r"href=\"\?post=(.*?)\">")

title = "1234567890"
body="abcdefghijk"


p = requests.post("http://35.227.24.107/51980f8ea3/", data={
                                                        'title':title,
                                                        'body':body
                                                    }, proxies={'http':'http://127.0.0.1:8080'}, allow_redirects=False)
if not p.ok:
    print('error generando hash : ')
    print(p.text)
    print(p.status_code)
    sys.exit(1)
html = p.text
m = rhash.search(html)
if not m:
    print('algo salió mal extrayendo el hash')
    sys.exit(1)
hash_ = m.group(1)
print(hash_)

dhash = common.b64d(hash_)
nhash = dhash[16:0] + dhash[:16]
print(binascii.hexlify(dhash))
print(binascii.hexlify(nhash))

hash_ = common.b64e(nhash)
print(hash_)
r = requests.get(f'http://35.227.24.107/51980f8ea3/?post={hash_}',  proxies={'http':'http://127.0.0.1:8080'}, allow_redirects=False)
print(r.text)