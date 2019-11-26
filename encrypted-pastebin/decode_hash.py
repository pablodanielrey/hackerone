
import sys
import binascii
from common import b64d, desencriptar


hash_ = "oUB6rGtE!MrULoYPlTGggbSADE33kFcPCpgyB2v3cqOdpumeP7pnUWOR7!7UZk!Qfd4cB72JAQTZuOjK5HXBFO2t5eii5Vsl6LZFhsECZNCIf1qLan1NDVydYkI2oF-h!YmS5rhwATnnaqy7ctKSlIPwgt1s9!KmloPGKbeJhAhITswuDPQd2QVarxIO2L2YTnt6w8E-8Qksyo-eqaJsnQ~~"
d_ = b64d(hash_)
print(binascii.hexlify(d_))


deadbeefcafe0123
feedface456789ab ---- decrypt ----> 1234567x

x ^0x23 == 0x7

0x1

