import argparse
from DES_Pack.generateKey import generateKeys
from DES_Pack.des import feistel


def main():
    parser = argparse.ArgumentParser()
    group_key = parser.add_mutually_exclusive_group(required=True)
    group_mode = parser.add_mutually_exclusive_group(required=True)
    group_crypt = parser.add_mutually_exclusive_group()
    group_mode.add_argument(
        '--ECB',
        dest='mode',
        action='store_const',
        const=1
    )
    group_mode.add_argument(
        '--CBC',
        dest='mode',
        action='store_const',
        const=2
    )
    group_key.add_argument(
        '-g', '--generate-key',
        dest='key',
        action='store_false',
        help="generate all keys from one key"
    )
    group_key.add_argument(
        '-r', '--read-key',
        dest='key',
        action='store_true',
        help="read all keys from file"
    )
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
    # print(args)
    keys = []
    with open(args.key_file, 'rb') as key_file:
        if args.key:
            print('read keys ', args.key_file)
            # read 16 times a key
            for i in range(16):
                keys.append(int.from_bytes(key_file.read(8), 'big'))
        else:
            # genreate all keys out of one
            print('generate keys ', args.key_file)
            generate_file = int.from_bytes(key_file.read(8), 'big')
            keys = generateKeys(generate_file)
    if args.decrypt:  # reverse the list of keys
        print('reversing keys')
        keys.reverse()

    if args.mode == 1:
        gen_crypt = ecb(args.input_file, keys)
    elif args.mode == 2:
        if args.decrypt:
            gen_crypt = cbc_decrypt(args.input_file,keys)
        else:
            gen_crypt = cbc(args.input_file, keys)
    print('encrypting to ', args.output_file)
    with open(args.output_file, 'wb') as output_file:
        for cypher in gen_crypt:
            output_file.write(cypher.to_bytes(16, 'big'))
    print('DONE')


def ecb(file, keys):
    with open(file, 'rb') as open_file:
        m = open_file.read(16)
        while len(m) == 16:
            m = int.from_bytes(m, 'big')
            yield feistel(m, keys)
            m = open_file.read(16)
        if len(m) > 0:
            m = int.from_bytes(m + b' ' * (16 - len(m)), 'big')
            yield feistel(m, keys)


def cbc(file, keys):
    with open(file, 'rb') as open_file:
        m = open_file.read(16)
        y = 0
        while len(m) == 16:
            m = int.from_bytes(m, 'big')
            y = feistel(m ^ y, keys)
            yield y
            m = open_file.read(16)
        if len(m) > 0:
            m = int.from_bytes(m + b' ' * (16 - len(m)), 'big')
            yield feistel(m ^ y, keys)


def cbc_decrypt(file, keys):
    with open(file, 'rb') as open_file:
        m = open_file.read(16)
        y = 0
        while len(m) == 16:
            m = int.from_bytes(m, 'big')
            y = feistel(m, keys) ^ y
            yield y
            y = m
            m = open_file.read(16)
        if len(m) > 0:
            m = int.from_bytes(m + b' ' * (16 - len(m)), 'big')
            yield feistel(m, keys) ^ y


if __name__ == '__main__':
    main()
