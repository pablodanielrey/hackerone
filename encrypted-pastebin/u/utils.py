import requests
import binascii
import re
rhash = re.compile(r"href=\"\?post=(.*?)\">")
rtitle = re.compile(r"<h1>(.*?)</h1>")
rbody = re.compile(r"<pre>\n*(.*?)\n*</pre>", re.MULTILINE | re.S)

import u.common

def extract_hash(text):
    m = rhash.search(text)
    if not m:
        return None
    return m.group(1)

def extract_data(text):
    t = rtitle.search(text)
    b = rbody.search(text)
    return (t.group(1) if t else None, b.group(1) if b else None)

def print_hash(h):
    print(binascii.hexlify(h).decode('utf8'))


def xx(iv, data):
    rs = [0] * len(data)
    for i,d in enumerate(data):
        x = iv[i]
        rs[i] = x ^ d
    return rs


def test_hash(url, hash):
    r = requests.get(f'{url}?post={hash}',  proxies={'http':'http://127.0.0.1:8080'}, allow_redirects=False)
    return r.text


def encrypt_data(url, title, body, proxy=True):
    if proxy:
        p = requests.post(url, data={ 'title':title, 'body':body }, proxies={'http':'http://127.0.0.1:8080'}, allow_redirects=False)
    else:
        p = requests.post(url, data={ 'title':title, 'body':body }, allow_redirects=False)
    #p = requests.post(url, data={ 'title':title, 'body':body }, allow_redirects=False)
    hash_ = extract_hash(p.text)
    dhash = u.common.b64d(hash_)
    return dhash

def decript_data(url, hash):
    ehash = u.common.b64e(hash)
    r = requests.get(f'{url}?post={ehash}',  proxies={'http':'http://127.0.0.1:8080'}, allow_redirects=False)
    #r = requests.get(f'{url}?post={ehash}',  allow_redirects=False)
    if 'PaddingException' in r.text:
        raise Exception('error de padding')
    return r.text