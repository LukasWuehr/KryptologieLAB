import argparse


def generateKeys(key, rounds=16, key_length=46):
    # split key
    keys = []
    piece_length = key_length // 2  # 32
    mask_rotate = 2 ** (piece_length - 2) - 1  # 0x3fffffff
    mask = 2 ** piece_length - 1  # 0xffffffff
    left_piece = key >> piece_length
    right_piece = key & mask

    for i in range(rounds):
        # rotate left 2
        left_overlap = left_piece >> (piece_length - 2)  # 2 highest bit
        left_piece = ((left_piece & mask_rotate) << 2) | left_overlap  # cut 2 highest bit, shl2, add 2 highest bit

        left_overlap = right_piece >> (piece_length - 2)  # 2 highest bit
        right_piece = ((right_piece & mask_rotate) << 2) | left_overlap  # cut 2 highest bit, shl2, add 2 highest bit

        # permutation
        perm_list = [39, 46, 57, 29, 50, 36, 14, 8, 45, 31, 53, 21, 56, 55, 32, 30, 16, 38, 47, 37, 7, 5, 27, 49, 48,
                     58, 26, 42, 60, 23, 12, 44, 24, 17, 6, 54, 2, 34, 62, 35, 22, 15, 4, 43, 40, 11, 51, 52, 1, 33, 28,
                     61, 18, 13, 59, 19, 0, 41, 20, 10, 3, 9, 25, 63]
        # with open('permutation.txt', 'r') as permutation:  # read permutation file and format
        #    perm_list = permutation.read().strip(' []\n').split(',')
        # perm_list = [int(e) for e in perm_list]
        org_key = (left_piece << piece_length) | right_piece  # put both pieces together
        round_key = 0
        # permute the key
        for pos in range(len(perm_list)):
            bit = (org_key >> pos) & 1  # bit is on first position
            round_key |= (bit << perm_list[pos])  # bit is on new pos and added to round key
        keys.append(round_key)
    return keys


def readKey(file):
    with open(file, 'rb') as open_file:
        text = open_file.read(8)
        print(text.hex())
        return int.from_bytes(text, 'little')


# only for testing purpose
def bitLen(int_type):
    length = 0
    while int_type:
        int_type >>= 1
        length += 1
    return length


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input',
        type=readKey,
        nargs='?'
    )
    parser.add_argument(
        'output',
        type=str,
        nargs='?'
    )
    parser.add_argument(
        '-r', '--rounds',
        type=int,
        default=16
    )
    parser.add_argument(
        '-l', '--length',
        type=int,
        default=64
    )
    args = parser.parse_args()
    with open(str(args.output), 'wb') as out:
        [out.write(key.to_bytes(8,'little')) for key in generateKeys(args.input, args.rounds, args.length)]
    print(args)