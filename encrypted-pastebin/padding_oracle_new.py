
from padding_oracle.padding_oracle import padding_oracle
from server import main
from u.common import b64e, b64d

def decrypt(data:memoryview) -> bytes:
    global iv
    data_to_send = bytes(data) + iv
    de = b64e(data_to_send)
    return main.process_request(de)

def check_padding_error(d) -> bool:
    return type(d) is str and 'PaddingException' in d


if __name__ == '__main__':
    coded_hash = main.process_get()
    hashi_ = b64d(coded_hash)
    iv = hashi_[-16:]
    hash_ = hashi_[:-16]

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
    print(decrip.decode('utf8'))