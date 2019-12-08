
from padding_oracle.padding_oracle import padding_oracle
from server import main
from u.common import b64e, b64d

iv = [0] * 16

def decrypt(data:memoryview) -> bytes:
    global iv
    data_to_send = iv + bytes(data)
    de = b64e(data_to_send)
    return main.process_request(de)

def check_padding_error(d) -> bool:
    return type(d) is str and 'PaddingException' in d


def ejecutar_padding_oracle(hashi_):
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



if __name__ == '__main__':
    coded_hash = main.process_get()
    hashi_ = b64d(coded_hash)
    """
    decrip = ejecutar_padding_oracle(hashi_)

    #imprimo el hash por bloque.
    for i in range(0, len(decrip), 16):
        bloque = int(i / 16)
        print(f'{bloque:02x}    {decrip[i:i+16]}')

    """

    """
        realizo un segundo ataque ya que tengo los caracteres decodificados, puedo calcular los caracteres 
        que quiero que resulten en el primer bloque!!!
        nuevo_iv = iv ^ p1 ^ caracteres_deseados
    """

    #elimino los bloques que no necesito
    hashi_ = hashi_[16*5:]
    decrip = ejecutar_padding_oracle(hashi_)

    #imprimo el hash por bloque.
    for i in range(0, len(decrip), 16):
        bloque = int(i / 16)
        print(f'{bloque:02x}    {decrip[i:i+16]}')

    #calculo los xors con los caracteres finales deseados para generar el nuevo IV.
    caracteres = b'{"id":"111111111'
    antiguo_iv = hashi_[:16]
    p1 = decrip[:16]

    print('calculando nuevo IV')
    nuevo_iv = [0] * 16
    for i in range(16):
        nuevo_iv[i] = antiguo_iv[i] ^ p1[i] ^ caracteres[i]
        print(f'{nuevo_iv[i]:02x} <-- {antiguo_iv[i]:02x} ^ {p1[i]:02x} ^ {caracteres[i]:02x}')
    print(bytes(nuevo_iv).hex())

    nuevo_hash = bytes(nuevo_iv) + hashi_[16:]
    decrip = ejecutar_padding_oracle(nuevo_hash)

    #imprimo el hash por bloque.
    for i in range(0, len(decrip), 16):
        bloque = int(i / 16)
        print(f'{bloque:02x}    {decrip[i:i+16]}')
