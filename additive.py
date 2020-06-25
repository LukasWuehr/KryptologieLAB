import getopt
import sys

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # used alphabet


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hedb:", ["encrypt=", "decrypt=", "bruteforce="])  # input arguments
    except getopt.GetoptError:  # error
        print('additive.py -[e,d] <inputfile>  <outputfile> <key>')
        sys.exit(2)

    input_file = open(argv[1], 'r')
    input_text = input_file.read()
    input_file.close()
    output_text = ''

    for opt, arg in opts:  # choose the option
        if opt == '-h':  # help
            print('additive.py -[e,d] <inputfile>  <outputfile> <key>')
            sys.exit()
        elif opt in ("-e", "--encrypt"):  # encrypt
            output_text = encrypt(argv[3], input_text)
        elif opt in ("-d", "--decrypt"):  # decrypt
            output_text = decrypt(argv[3], input_text)
        elif opt in ("-b", "--bruteforce"):  # all possible keys
            for key in range(1, len(alphabet)):
                output_text += str(key) + ": " + decrypt(key, input_text) + "\n"

        print(output_text)  # writing
        outputFile = open(argv[2], 'w')
        outputFile.write(output_text)
        outputFile.close()


def encrypt(key, text):  # encryption of text
    rotate_alphabet = ''
    length = len(alphabet)
    for numb in range(0, length):  # create shifted alphabet
        rotate_alphabet += alphabet[(numb + int(key)) % length]
    return text.translate(str.maketrans(alphabet, rotate_alphabet))  # translation with table


def decrypt(key, text):  # decryption of text
    rotate_alphabet = ''
    length = len(alphabet)
    for numb in range(0, length):  # create shifted alphabet
        rotate_alphabet += alphabet[(numb - int(key)) % length]
    return text.translate(str.maketrans(alphabet, rotate_alphabet))  # translation with table


if __name__ == "__main__":
    main(sys.argv[1:])
