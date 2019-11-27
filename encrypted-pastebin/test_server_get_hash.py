
import binascii

import server.main
import u.common

if __name__ == '__main__':
    bhash = server.main.process_get()
    print(f"Hash final retornado al cliente ({len(bhash)}) {bhash}")