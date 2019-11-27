
import binascii

import server.main
import u.common

if __name__ == '__main__':

    print('####################\nObteniendo hash desde el servidor\n##################')

    bhash = server.main.process_get()
    print(f"Hash obtenido {bhash}")

    print('####################\nDesencriptando el hash\n#####################')

    j = server.main.process_request(bhash)

    print(f"Datos obtenidos {j}")