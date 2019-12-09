
hash_ = bytes.fromhex('952c3f86b97a4037ea46b813602dc8b74e6ad025ea495cbb46292c392b26d0c6f0eb5179596bbdbbecb87899be55919a8a80b8b55dfbaecf39256e0b4236607c696ba958ec619892d26c52396a86423672d0b3c396a2437020e4df82d90572ed886b59b494355f23f1cf7e38151e4930a32ec7fc6895c2accfac7d6c001f293e1b907958cfe4a1ca8d11646c890aa430')
decrypted_bytes = bytes.fromhex('24464c414724222c20226964223a202232222c20226b6579223a20227834346f57334e586766763144384d59785a786c4c517e7e227d0a0a0a0a0a0a0a0a0a0a')

chopped_hash_ = hash_[-(16*3):]
iv = chopped_hash_[:16]
new_hash_ = chopped_hash_[16:]
decrypted_to_work = decrypted_bytes[-16:]

decrypted = b'$FLAG$", "id": "2", "key": "x44oW3NXgfv1D8MYxZxlLQ~~"}'


caracteres = b'{"id":"1", "a":"'
padding = [16 - len(caracteres)] * (16 - len(caracteres))
#caracteres = caracteres + bytes(padding)

def print_blocks(d):
    for i in range(0, len(d), 16):
        bloque = int(i / 16)
        if type(d) is str:
            print(f'{bloque:02x}    {d[i:i+16]}')
        else:
            print(f'{bloque:02x}    {d.hex()[i:i+16]}')


print_blocks(new_hash_)
print_blocks(decrypted_to_work)

import requests
from padding_oracle.padding_oracle import calculate_new_iv
from u.common import b64e, b64d


key = 'x44oW3NXgfv1D8MYxZxlLQ~~'
print('KEY:')
print(b64d(key).hex())

url = 'http://34.74.105.127/71a7d1053f/'
new_iv = calculate_new_iv(iv, decrypted_to_work, caracteres)

data_to_send = new_iv + new_hash_


print('Enviando al servidor el nuevo hash calculado')
print(data_to_send.hex())

de = b64e(data_to_send)
r = requests.get(f'{url}?post={de}',  proxies={'http':'http://127.0.0.1:8080'}, allow_redirects=False)
#r = requests.get(f'{url}?post={de}',  allow_redirects=False)
print(r.text)
