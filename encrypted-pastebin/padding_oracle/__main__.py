from random import randrange
from .enc import encrypt, pad, print_block, PaddingException, decrypt
from .padding_oracle import padding_oracle

def decrypte(data:memoryview) -> bytes:
    try:
        return decrypt(bytes(data))
    except PaddingException:
        return 'PaddingException'

def check_padding_error(d):
    if type(d) is str and 'PaddingException' in d:
        return True
    return False


def test_padding_oracle():
    blocks = 5
    extra = 12

    block_to_encrypt = pad(bytes([randrange(255) for _ in range((16*blocks) + extra)]))
    h_ = encrypt(block_to_encrypt)
    hash_ = memoryview(h_)

    print(f'bloque a encriptar : {block_to_encrypt.hex()}')
    print(f'bloque encriptado  : {h_.hex()}')

    decrypted = None

    for b in range(blocks):
        i = b * 16
        f = i + 16
        c1 = hash_[i:f]
        c2 = hash_[f:f+16]
        des = padding_oracle(c1, c2, decrypte, check_padding_error)
        if not decrypted:
            decrypted = des
        else:
            decrypted = decrypted + des

    print(f'bloque original      : {block_to_encrypt[16:].hex()}')
    print(f'bloque desencriptado : {decrypted.hex()}')


test_padding_oracle()