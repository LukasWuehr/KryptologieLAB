import argparse
from DES_Pack.generateKey import generateKeys


def main():
    parser = argparse.ArgumentParser()
    group_key = parser.add_mutually_exclusive_group(required=True)
    group_crypt = parser.add_mutually_exclusive_group()
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
    #print(args)
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

    print('read text ', args.input_file)
    with open(args.input_file, "rb") as input_file:
        input = int.from_bytes(input_file.read(16), 'big')

    print('encrypt/decrypt text')
    output = feistel(input, keys)

    print('save new text in ', args.output_file)
    with open(args.output_file, 'wb') as output_file:
        output_file.write(output.to_bytes(16, 'big'))
    print('DONE')


def feistel(input, keys):
    mask = 2 ** 64 - 1  # 2/128 bit
    left = input >> 64
    right = input & mask

    for key in keys:
        left_temp = right  # new left text piece
        right = left ^ f_box(right, key)  # xor of left and fbox
        left = left_temp
    output = (right << 64) | left  # last switch
    return output


def f_box(input, key):
    input = input ^ key  # xor text with roundkey

    output = 0
    mask = 2 ** 8 - 1  # first8 bit 1
    # split text in 8x8bit for sbox
    for byte in range(8):
        input_byte = input >> (byte * 8)
        input_byte = input_byte & mask
        s_box_byte = s_box(input_byte)
        output = output | (s_box_byte << (byte * 8))
    return output


def s_box(input):
    sBox_permutation = [229, 25, 220, 149, 5, 69, 246, 195, 210, 19, 89, 116, 170, 147, 166, 30, 28, 254, 15, 59, 247,
                        81, 73, 231, 248, 235, 6, 105, 151, 102, 179, 150, 228, 126, 171, 22, 61, 128, 79, 215, 1, 0,
                        24, 100, 17, 183, 67, 35, 68, 31, 146, 239, 38, 184, 107, 23, 65, 63, 51, 27, 255, 122, 165, 37,
                        226, 57, 221, 84, 187, 76, 207, 173, 16, 142, 111, 244, 87, 188, 118, 211, 224, 214, 137, 141,
                        222, 192, 3, 113, 201, 88, 234, 33, 139, 191, 36, 40, 29, 135, 249, 20, 237, 34, 124, 14, 186,
                        43, 108, 26, 197, 198, 103, 98, 180, 45, 39, 253, 110, 185, 4, 7, 54, 205, 52, 64, 223, 162,
                        189, 219, 75, 172, 18, 93, 50, 194, 119, 160, 145, 250, 117, 153, 161, 114, 206, 13, 83, 58, 94,
                        148, 32, 121, 251, 240, 53, 217, 101, 144, 130, 177, 243, 10, 196, 245, 12, 125, 134, 138, 133,
                        127, 155, 181, 74, 158, 60, 190, 174, 123, 242, 42, 202, 136, 44, 225, 8, 55, 159, 167, 70, 62,
                        109, 66, 86, 227, 157, 168, 71, 106, 178, 104, 212, 99, 82, 143, 238, 80, 140, 152, 85, 47, 203,
                        46, 182, 21, 129, 92, 204, 90, 97, 9, 230, 2, 200, 131, 91, 164, 169, 252, 208, 216, 11, 241,
                        154, 41, 156, 236, 72, 120, 193, 199, 175, 49, 56, 78, 95, 115, 77, 232, 132, 209, 163, 96, 213,
                        48, 176, 112, 233, 218]

    return sBox_permutation[input]


if __name__ == '__main__':
    main()
