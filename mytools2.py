import hashlib
from pyfinite import ffield, genericmatrix
import random
import itertools
import functools
import sys

_PRIME = 2**127 - 1
_RINT = functools.partial(random.SystemRandom().randint, 0)

Htable = []
n = 100
P = _PRIME
F = ffield.FField(n)

def myGetRandomElement():
    return _RINT(P)

def mysub(x, y):
    return (x - y + P) % P

def myadd(x, y):
    return (x + y) % P

def mymul(x, y):
    return ((x%P)*(y%P))%P

def mydiv(x, y):
    return (x*(_extended_gcd(y,P)))%P

def _extended_gcd(a, b):
    '''
    division in integers modulus p means finding the inverse of the
    denominator modulo p and then multiplying the numerator by this
    inverse (Note: inverse of A is B such that A*B % p == 1) this can
    be computed via extended Euclidean algorithm
    http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
    '''
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a%b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x

def genMatrix(size:tuple, min=0, max=P):
    if not isinstance(size, tuple) or len(size) !=2:
        raise Exception('Matrix size error')
    v = genericmatrix.GenericMatrix(size, zeroElement=0, identityElement=1, add=lambda x,y:(x+y)%P,
                                    sub=lambda x,y:(x-y+P)%P, mul=mymul, div=lambda x,y:(x*(_extended_gcd(y,P)))%P)
    row, col = size
    for r in range(row):
        tempcol = [random.randint(min, max) for c in range(col)]
        v.SetRow(r, tempcol)
    return v

def byteMatrix(m):
    r = 0
    row, col = m.Size()
    for i in range(row):
        for j in range(col):
            r += sys.getsizeof(m[i, j])
    r += sys.getsizeof(m)
    return r

def read_index(num_file):
    word_space = []
    with open('index_test', 'r') as f:
        for line in f:
            if num_file == 0:
                break
            num_file -= 1
            temp = line.strip('\n').split(' ')
            word_space.append(temp[1:])
    return word_space


with open('index_test', 'r') as f:
    for line in f:
        temp = line.strip('\n').split(' ')
        for word in temp[1:]:
            if word not in Htable:
                Htable.append(word)
def hs(w):
    #return sum([ord(ch) for ch in w])
    # if w not in Htable:
    #     return int.from_bytes(hashlib.sha256(bytes(w, encoding='utf-8')).digest(), byteorder='little')%P + len(Htable)
    # return (Htable.index(w)+1)
    return int.from_bytes(hashlib.sha256(bytes(w, encoding='utf-8')).digest(), byteorder='little')%P

def mypow(a, b, p=P):
    r = 1
    for i in range(b):
        r *= a
        r %= P
    return r

def test_Q_I(QQ=None, II=None):

    # H_Q_list = [mysub(0, 3598), mysub(0, 2), mysub(0, 3), mysub(0, 34555555555)]
    H_Q_list = [mysub(0, hs('ferc')), mysub(0, hs('eee')), mysub(0, hs('eee'))]
    Q = [coff(H_Q_list, i) for i in range(0, len(H_Q_list)+1)]
    if QQ is not None:
        Q = QQ
    mq = genMatrix((1, len(Q)))
    mi = genMatrix((mq.Size()[1], 1))

    mq.SetRow(0, Q)
    if II is not None:
        for i in range(mi.Size()[0]):
            mi.SetRow(i, [II[i]])
    else:
        for i in range(mi.Size()[0]):
            mi.SetRow(i, [mypow(hs('eee'), i)])
    print(mq)
    print(mi)
    print(mq*mi)
    #
    # H_Q_list = [-1, -2, -3, -555]
    #
    # Q = [coff(H_Q_list, i) for i in range(0, len(H_Q_list)+1)]
    # mq = Q
    # mi = []
    #
    # for i in range(len(mq)):
    #     mi.append(555**i)
    # r = 0
    # for i in range(len(mq)):
    #     r += (mq[i]*mi[i])
    #
    # print(mq)
    # print(mi)
    # print(r)

def coff(list, i):
    d = len(list)
    if d-i == 0:
        return 1
    result = 0
    for item in itertools.combinations(list, d-i):
        temp = 1
        for i_item in item:
            # temp = F.Multiply(temp, i_item)
            temp = mymul(temp, i_item)
            # temp*=i_item
        # result =F.Add(result, temp)
        result = myadd(result, temp)
        # result+=temp
    return result

def test_coff():
    print(coff([1,1,1], 3))


if __name__ == '__main__':
    # for i in itertools.combinations([1, 1, 2], 0):
    #     print(i)
    test_Q_I()

