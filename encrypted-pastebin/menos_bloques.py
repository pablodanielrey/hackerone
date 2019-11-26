
import utils

url = 'http://35.227.24.107/b6b38fea92/'

hash_ = utils.encript_data(url, 'aa', 'bb')
lhash = list(hash_)
hash__ = bytes(lhash[0:16] + lhash[-32:])
(t,b) = utils.decript_data(url, hash__)
print(t)
print(b)