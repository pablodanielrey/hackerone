
import sys
import json

hash_file = 'hash.json'
try:
    hash_file = sys.argv[1]
except Exception as e:
    pass

with open(hash_file, 'r') as f:
    hash_data = json.loads(f.read())

print(f"Trabajando con {hash_data}")