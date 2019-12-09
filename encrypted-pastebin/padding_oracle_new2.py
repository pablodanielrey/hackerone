
from padding_oracle.padding_oracle import padding_oracle, encrypt_padding_oracle
from server import main
from u.common import b64e, b64d

iv = bytes([0] * 16)

def decrypt(data:memoryview) -> bytes:
    global iv
    data_to_send = iv + bytes(data)
    de = b64e(data_to_send)
    return main.process_request(de)

def check_padding_error(d) -> bool:
    return type(d) is str and 'PaddingException' in d


def ejecutar_padding_oracle_enc(hashi_):
    global iv
    iv = hashi_[:16]
    hash_ = hashi_[16:]

    print(iv.hex())
    print(hash_.hex())

    decrip = None
    for i in range(len(hash_), 0, -16):
        print('-'*16)
        print(f'Pasada {i}')
        print('-'*16)

        if i-32 < 0:
            print('Procesando IV')
            c1 = iv
            c2 = hash_[:16]
        else:
            ini = i-32
            fin = ini+16
            c1 = hash_[ini:fin]
            c2 = hash_[fin:fin+16]
        des = padding_oracle(c1, c2, decrypt, check_padding_error)
        if not decrip:
            decrip = des
        else:
            decrip = des + decrip
        print(decrip.hex())
        try:
            print(decrip.decode('utf8'))
        except Exception:
            pass
    #print(decrip.decode('utf8'))
    return decrip


def pad(data):
    pad_byte = 16 - (len(data) % 16)
    return data + bytes(pad_byte for i in range(pad_byte))

def obtener_bloques(data:bytes) -> [bytes]:
    bloques = []
    for i in range(0, len(data), 16):
        bloques.append(data[i:i+16])
    return bloques

if __name__ == '__main__':

    plaintext = pad(b'{"r":"asdasd","d":"sddsf"}')
    plains = obtener_bloques(plaintext)

    coded_hash = main.process_get()
    hashi_ = b64d(coded_hash)
    last_block = hashi_[-16:]
    
    c2 = last_block
    ces = None
    for i in range(len(plains)-1,-1,-1):
        p2 = plains[i]
        ce = encrypt_padding_oracle(c2, p2, decrypt, check_padding_error)
        c2 = ce
        if not ces:
            ces = ce
        else:
            ces = ce + ces
        
    print(ces.hex())
    print(type(ces))

    encoded = b64e(ces)

    print(main.process_request(encoded))