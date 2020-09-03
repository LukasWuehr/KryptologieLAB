import random as rd
import secrets


def randomPrime(key_size):
    while True:
        n = secrets.randbits(key_size)
        if rabin(n):  # and n % 2 == 0:
            return n


def distinctPrimes(size: int):
    distinct = False
    good_range = False
    while (not distinct) or (not good_range):
        p = randomPrime(size)
        q = randomPrime(size)
        distinct = p != q  # distinct
        phi = (p - 1) * (q - 1)
        n = p * q
        # python has no int limit
        good_range = 2**32 - 1 < n <= 2**64 - 1  # big enough and still unsigned int (64 bit) #size max 32
    return phi, n


def keys(size):
    phi, n = distinctPrimes(size)
    while gcd(3, phi) != 1:
        phi, n = distinctPrimes(size)
    e = 3
    d = eEuklid(e, phi)
    # print((e*d)%phi)  # =1
    return n, e, d


def eEuklid(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m

    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def rabin(n: int):
    k: int = 0
    m: int = n - 1
    while (m % 2 == 0):
        k += 1
        m >>= 1
    for trails in range(5):
        a: int = rd.randint(2, n)
        b: int = pow(a, m, n)
        if b % n == 1:
            return True
        for i in range(1, k):
            if b % n == -1:
                return True
            else:
                b = pow(b, 2, n)
    return False


def gcd(a, b):
    while b != 0:
        t = b
        b = a % b
        a = t
    return a


def saveKeys(size, public, private):
    n, e, d = keys(size)
    print(n, e, d)
    n = n.to_bytes(8, 'big')
    e = e.to_bytes(e.bit_length()//8+1, 'big')
    d = d.to_bytes(d.bit_length()//8+1, 'big')

    with open(public, 'wb') as pub_file:
        pub_file.write(n + e)
    with open(private, 'wb') as pvt_file:
        pvt_file.write(n + d)


if __name__ == '__main__':
    print(saveKeys(32, 'public.txt', 'prvate.txt'))
