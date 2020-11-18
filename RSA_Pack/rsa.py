import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    group_crypt = parser.add_mutually_exclusive_group()
    parser.add_argument(
        'key_file',
        type=str,
        help="file containing key|s"
    )
    parser.add_argument(
        'input_file',
        type=str,
        help="file containing text to encrypt"
    )
    parser.add_argument(
        'output_file',
        type=str,
        help="file containing encrypted text"
    )
    group_crypt.add_argument(
        '-e', '--encrypt',
        dest='decrypt',
        action='store_false',
        default=False,
        help="encrypt"
    )
    group_crypt.add_argument(
        '-d', '--decrypt',
        action='store_true',
        default=False,
        help="decrypt"
    )
    args = parser.parse_args()
    n,k = key(args.key_file)
    if args.decrypt:
        decrypt(args.input_file,args.output_file, n, k)
    else:
        encrypt(args.input_file,args.output_file, n, k)



def key(file):
    with open(file, 'rb') as key_file:
        n = int.from_bytes(key_file.read(8), 'big')
        k = int.from_bytes(key_file.read(), 'big')
    return n, k


def text(file, chunk):
    with open(file, 'rb')as text_file:
        m = text_file.read(chunk)
        while len(m) == chunk:
            yield int.from_bytes(m, 'big')
            m = text_file.read(chunk)
        if len(m) > 0:
            yield int.from_bytes(m + b' ' * (chunk - len(m)), 'big')


def encrypt(file, dest_file, n, k):
    text_gen = text(file, 4)
    if os.path.exists(dest_file):  # begin with empty file
        os.remove(dest_file)
    with open(dest_file, 'ab') as dest:
        for m in text_gen:
            dest.write(exp2(m, k, n).to_bytes(8, 'big'))


def decrypt(file, dest_file, n, k):
    text_gen = text(file, 8)
    if os.path.exists(dest_file):  # begin with empty file
        os.remove(dest_file)
    with open(dest_file, 'ab') as dest:
        for m in text_gen:
            dest.write(exp2(m, k, n).to_bytes(4, 'big'))


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
            x = (x * m) % n
        k >>= 1
        m = m ** 2 % n
    return x


if __name__ == '__main__':
    main()
