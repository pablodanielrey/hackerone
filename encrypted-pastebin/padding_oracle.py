
import sys
import json
import binascii


def save_progress(pad_data):
    with open('padding_oracle.json', 'w') as log:
        log.write(json.dumps(pad_data))



hash_file = 'hash.json'
try:
    hash_file = sys.argv[1]
except Exception as e:
    pass

with open(hash_file, 'r') as f:
    hash_data = json.loads(f.read())



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
    'decoded_bytes': '',
    'decoded_string': ''
}
for block_index in range(initial_block, blocks, 1):
    padding_oracle_data['working_block'] = block_index
    i = block_index * 16
    f = i + 16
    block_data = hash_[i:f]

    working_buffer = memoryview(bytearray(hash_))
    working_block = working_buffer[i:f]

    print(f'Procesando bloque : {block_index}')
    print(f"Bloque    : {binascii.hexlify(block_data).decode('utf8')}")
    print(f"Working   : {binascii.hexlify(working_block).decode('utf8')}")

    #para cada uno de los bytes del bloque
    for b in range(16):
        byte_found = False
        pos = 15 - b
        print(f'Procesando bloque {block_index} byte {pos}')
        padding_oracle_data['working_byte'] = pos
        save_progress(padding_oracle_data)

        #para cada valor del byte que no es el original
        for c in range(256):
            if c != block_data[pos]:
                working_block[pos] = c
                print(binascii.hexlify(working_block).decode('utf8'))
                # aca testeo si no tira padding error
                #byte_found = True
                #break

        #pruebo con el byte original
        if not byte_found:
            working_block[pos] = block_data[pos]
            print(binascii.hexlify(working_block).decode('utf8'))
            byte_found = True

        if not byte_found:
            raise Exception(f'No se pudo encontrar solución al bloque {block_index} byte {pos}')

    padding_oracle_data['blocks_decoded'].append(block_index)
    save_progress(padding_oracle_data)