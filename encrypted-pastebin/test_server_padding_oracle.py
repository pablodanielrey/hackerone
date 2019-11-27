
import sys
import json
import binascii

import server.main
import u.utils


def decript_data(data):
    """ llama al servidor y trata de desencriptar el hash """
    ehash = u.common.b64e(data)
    p = server.main.process_request(ehash)
    return p


# obtengo un hash válido desde el server virtual
h_ = server.main.process_get()
hash_b = u.common.b64d(h_)
hash_data = binascii.hexlify(hash_b)
hash_ = memoryview(hash_b)

decoded_bytes = [0] * len(hash_)

blocks = int(len(hash_) / 16)
initial_block = blocks -1 

print(f"Trabajando con \n {hash_data}")
print(f"Longitud del hash : {len(hash_data)}")
print(f"Cantidad de bloques : {blocks}")
print(f"Bloque Inicial : {initial_block}")

padding_oracle_data = { 
    'hash_data': hash_data,
    'working_block': 0,
    'working_byte': 0,
    'blocks_decoded': [],
    'decoded_bytes': bytearray(len(hash_))
}

for block_index in range(initial_block, 0, -1):
    padding_oracle_data['working_block'] = block_index
    i = block_index * 16
    f = i + 16
    block_data = hash_[i:f]
    decoded_bytes = memoryview(padding_oracle_data['decoded_bytes'])[i:f]
    working_buffer = memoryview(bytearray(hash_))
    #sending_buffer = working_buffer[:f+16]
    working_block = working_buffer[i:f]

    print(f'Procesando bloque : {block_index}')
    print(f"Bloque    : {binascii.hexlify(block_data).decode('utf8')}")
    print(f"Working   : {binascii.hexlify(working_block).decode('utf8')}")
    #print(f"To Send   : {binascii.hexlify(sending_buffer).decode('utf8')}")

    #para cada uno de los bytes del bloque
    for b in range(16):
        byte_found = False
        pos = 15 - b

        print(f'Procesando bloque {block_index} byte {pos}')
        padding_oracle_data['working_byte'] = pos

        # pruebo todos los valores de bytes, ultimo el valor original
        bytes_to_try = [x for x in range(0,block_data[pos])] + [x for x in range(block_data[pos]+1,256)] + [block_data[pos]]
        print(f"Bytes to try {bytes_to_try}")
        tries = 0
        for c in bytes_to_try:
            if byte_found:
                break
            working_block[pos] = c
            #print(binascii.hexlify(sending_buffer).decode('utf8'))
            print(binascii.hexlify(hash_).decode('utf8'))
            print(binascii.hexlify(working_buffer).decode('utf8'))
            print(binascii.hexlify(padding_oracle_data['decoded_bytes']).decode('utf8'))
            try:
                r = decript_data(working_buffer)
                if 'PaddingException' in r:
                    raise Exception()

                print(f"Encontrado {c:02x} para {block_index} en la pos {pos}")

                padding = 16 - pos
                decoded_bytes[pos] = block_data[pos] ^ working_block[pos] ^ padding
                print(f"Decodificado {decoded_bytes[pos]:02x} Original {block_data[pos]:02x} Actual {working_block[pos]:02x} Padd {padding:02x}")

                #corrijo el padding para el bloque en proceso.        
                for pad in range(pos,16):
                    working_block[pad] = decoded_bytes[pad] ^ block_data[pad] ^ (padding + 1)
                    print(f"Woking Block con padding : {binascii.hexlify(working_block)}")

                byte_found = True
                print(binascii.hexlify(padding_oracle_data['decoded_bytes']))
                try:
                    print(padding_oracle_data['decoded_bytes'].decode('utf8'))
                except Exception:
                    pass
                break

            except Exception as e:
                tries += 1
                sys.stdout.write('.')
                sys.stdout.flush()
                pass

        if not byte_found:
            raise Exception(f'No se pudo encontrar solución al bloque {block_index} byte {pos}')

        print(binascii.hexlify(decoded_bytes))
        try:
            print(decoded_bytes.decode('utf8'))
        except Exception:
            pass

    padding_oracle_data['blocks_decoded'].append(block_index)

print(padding_oracle_data)