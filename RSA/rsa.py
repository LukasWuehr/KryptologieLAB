import argparse
import os


def key(file):
    with open(file, 'rb') as key_file:
        n = int.from_bytes(key_file.read(8), 'big')
        k = int.from_bytes(key_file.read(), 'big')
    return n, k


def text(file):
    with open(file, 'rb')as text_file:
        m = text_file.read(8)
        while len(m) == 8:
            yield int.from_bytes(m, 'big')
            m = text_file.read(8)
        if len(m) > 0:
            yield int.from_bytes(m, 'big') << ((8 - len(m)) * 8)


def cypher(file, dest_file, n, k):
    text_gen = text(file)
    if os.path.exists(dest_file):  # begin with empty file
        os.remove(dest_file)
    with open(dest_file, 'ab') as dest:
        for m in text_gen:
            print(m.to_bytes(8, 'big'))
            dest.write(exp2(m,k,n).to_bytes(8,'big'))


def exp(m, k, n):
    c = 1
    e = 0
    while e < k:
        c = (m * c) % n
        e += 1
    return c

def exp2(m, k, n):
    x = 1
    while k != 0:
        if k & 1 == 1:
            x = (x*m) % n
        k >>= 1
        m = m**2 % n
    return x


if __name__ == '__main__':
    print(key('prvate.txt'))
    print(key('public.txt'))
    n, k = key('public.txt')
    cypher('../DES/text.txt','crypto.txt', n,k)
    n, d = key('prvate.txt')
    cypher('crypto.txt', 'decrypto.txt', n, d)
