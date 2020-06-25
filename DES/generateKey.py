import sys


def generateKeys(key, rounds=16):
    # split key
    keys = []
    left_piece = key >> 32
    right_piece = (key & 0xffffffff)

    for i in range(rounds):
        # rotate left 2
        left_overlap = left_piece >> 30  # 2 highest bit
        left_piece = ((left_piece & 0x3fffffff) << 2) | left_overlap  # cut 2 highest bit, shl2, add 2 highest bit

        left_overlap = right_piece >> 30  # 2 highest bit
        right_piece = ((right_piece & 0x3fffffff) << 2) | left_overlap  # cut 2 highest bit, shl2, add 2 highest bit

        # permutation
        perm_list = [39, 46, 57, 29, 50, 36, 14, 8, 45, 31, 53, 21, 56, 55, 32, 30, 16, 38, 47, 37, 7, 5, 27, 49, 48, 58, 26, 42, 60, 23, 12, 44, 24, 17, 6, 54, 2, 34, 62, 35, 22, 15, 4, 43, 40, 11, 51, 52, 1, 33, 28, 61, 18, 13, 59, 19, 0, 41, 20, 10, 3, 9, 25, 63]
        #with open('permutation.txt', 'r') as permutation:  # read permutation file and format
        #    perm_list = permutation.read().strip(' []\n').split(',')
        #perm_list = [int(e) for e in perm_list]
        print(perm_list.index(2))
        org_key = (left_piece << 32) | right_piece  # put both pieces together
        round_key = 0
        # permute the key
        for pos in range(64):
            bit = (org_key >> perm_list[pos]) & 1  # bit is on first position
            round_key |= (bit << pos)  # bit is on new pos and added to round key
        keys.append(round_key)
    return keys


def readKey(file):
    with open(file, 'rb') as open_file:
        text = open_file.read(8)
        print(text.hex())
        return int.from_bytes(text, 'big')


# only for testing purpose
def bitLen(int_type):
    length = 0
    while int_type:
        int_type >>= 1
        length += 1
    return length


if __name__ == '__main__':
    o = open('bits.bin', 'wb')
    o.write(b'\xff\xff\xff\xff\xff\xff\xff\xf3')
    o.close()
    print(bitLen(42))
    print(generateKeys(42))
    print([x.to_bytes(byteorder='big', length=8).hex() for x in generateKeys(42)])

    try:
        if sys.argv[1] in ('-f', "--file"):
            key = readKey(sys.argv[2])
            print(key)
            print(generateKeys(key))
            print([x.to_bytes(byteorder='big', length=8).hex() for x in generateKeys(key)])
    except:
        pass
