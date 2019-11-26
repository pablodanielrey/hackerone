
import requests
import common
import utils

url = 'http://35.227.24.107/b6b38fea92/'

registers = []


for i in range(100):
    p = bytes([0 for _ in range(i)])
    try:
        ehash = common.b64e(p)
        r = requests.get(f'{url}?post={ehash}',  proxies={'http':'http://127.0.0.1:8080'}, allow_redirects=False)
        if 'IV must be 16 bytes long' in r.text:
            registers.append(i)
    except Exception as e:
        pass

print(registers)