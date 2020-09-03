import sys
from math import floor


def main():
    global crypto_file, sample_rh, sample_most_used_char, output_file
    try:
        if sys.argv[1] in ('-r', "--rauheit"):
            print(rauheit(open(sys.argv[2], 'r').read()))
            return
        elif sys.argv[1] in ('-a', "--automatic"):
            if sys.argv[2] in ('-l', "--lorem"):
                sample_rh = 0.0629611920940556
                sample_most_used_char = ' '
            else:
                sample_file = sys.argv[2]
                # get data of sample text
                sample = open(sample_file, 'r')
                sample_text = sample.read()
                sample.close()
                sample_rh = rauheit(sample_text)
                sample_most_used_char = most_used_chars(sample_text)
            crypto_file = sys.argv[3]
            output_file = sys.argv[4]
        elif (sys.argv[1] in ('-e', "--encrypt")):
            with open(sys.argv[2], 'r') as file:
                crypto_text = encrypt(file.read(),sys.argv[4])
            with open(sys.argv[3], 'w') as file:
                file.write(crypto_text)
            return
        elif (sys.argv[1] in ('-d', "--decrypt")):
            with open(sys.argv[2], 'r') as file:
                crypto_text = decrypt(file.read(),sys.argv[4])
            with open(sys.argv[3], 'w') as file:
                file.write(crypto_text)
            return

        elif (sys.argv[1] in ('-h', "--help")) | True:
            print("vigenereDecrypt.py -a <sampleLanguageFile> <encryptedFile> <outputFile>")
            return

    except:
        print("vigenereDecrypt.py -a <sampleLanguageFile> <encryptedFile> <outputFile>")
        sys.exit(2)

    # open and extract file content 0.0629611920940556 ' '
    crypto = open(crypto_file, 'r')
    crypto_text = crypto.read()
    crypto.close()

    # block size search
    for i in range(1, floor(len(crypto_text) / 4)):
        text_split = slice(crypto_text, i)  # split text into sections with same key
        text_split_rh = []
        for chars in text_split:  # get all rh
            text_split_rh.append(rauheit(chars))
        rh_sum = 0
        for rh in text_split_rh:  # average rh
            rh_sum += rh
        crypto_rh = rh_sum / len(text_split_rh)

        # test for right rh
        if abs(crypto_rh - sample_rh) <= 0.001:  # check if rh is almost same
            # search for individual key
            decrypt_key = key(text_split, sample_most_used_char)
            decrypt_text = decrypt(crypto_text, decrypt_key)
            print(decrypt_text)
            print('d: ', i, ' KEY: ', decrypt_key)
            if input('right decryption? y/n ') in ('y', "yes"):
                print('writing text to ', output_file)
                output_file_open = open(output_file, 'w')
                output_file_open.write(decrypt_text)
                output_file_open.close()
                print('DONE')
                sys.exit(0)
    print('No match found')
    return


def key(text_split, sample_muc, alph_size=128):
    decrypt_key = ''
    for chars in text_split:
        crypto_most_used_char = most_used_chars(chars)[0][0]  # most used cypher char
        key_part = chr((ord(crypto_most_used_char) - ord(sample_muc[0][0])) % alph_size)  # assumed key
        decrypt_key += key_part
    return decrypt_key


def rauheit(text, alph_size=128):
    icL = 0
    text = [ord(c) for c in text]
    for i in range(alph_size):
        # p(a)^2
        countChar = text.count(i) / len(text)
        icL += pow(countChar, 2)
    rh = icL - 1 / alph_size  # sum - 1/128
    return rh


def most_used_chars(text, alph_size=128):
    char_count = dict()
    # get number of all letters
    for i in range(alph_size):
        char_count[chr(i)] = text.count(chr(i))
    char_count_items = char_count.items()  # get all items as tuple
    char_count_items = sorted(char_count_items, key=lambda tup: tup[1], reverse=True)  # order desc
    return char_count_items


def slice(text, step=3):
    matrix = []
    for i in range(step):
        matrix.append(text[i::step])  # from i to end with step 'step'
    return matrix


def encrypt(text, encrypt_key, alph_size=128):
    key_length = len(encrypt_key)
    crypt_text = ''
    encrypt_key = [ord(c) for c in encrypt_key]
    text = [ord(c) for c in text]
    for numb in range(len(text)):
        crypt_text += chr((text[numb] + encrypt_key[numb % key_length]) % alph_size)
    return crypt_text


def decrypt(text, decrypt_key, alph_size=128):
    key_length = len(decrypt_key)
    crypt_text = ''
    decrypt_key = [ord(c) for c in decrypt_key]
    text = [ord(c) for c in text]
    for numb in range(len(text)):
        crypt_text += chr((text[numb] - decrypt_key[numb % key_length]) % alph_size)
    return crypt_text


if __name__ == '__main__':
    main()
