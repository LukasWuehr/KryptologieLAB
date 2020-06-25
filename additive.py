import sys, getopt

alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ' #used alphabet

def main(argv):
   try:
      opts, args = getopt.getopt(argv,"hedb:",["encrypt=","decrypt=","bruteforce="]) #input arguments
   except getopt.GetoptError: #error
      print( 'additive.py -[e,d] <inputfile>  <outputfile> <key>')
      sys.exit(2)

   inputFile = open(argv[1], 'r')
   inputText = inputFile.read()
   inputFile.close()
   outputText=''

   for opt, arg in opts:   #choose the option
      if opt == '-h':      #help
         print('additive.py -[e,d] <inputfile>  <outputfile> <key>')
         sys.exit()
      elif opt in ("-e", "--encrypt"): #encrypt
         outputText = encrypt(argv[3],inputText)
      elif opt in ("-d", "--decrypt"): #decrypt
         outputText = decrypt(argv[3],inputText)
      elif opt in ("-b", "--bruteforce"): #all possible keys
         for key in range(1,len(alphabet)):
            outputText += str(key)+": "+decrypt(key, inputText)+"\n"

      print(outputText) #writing
      outputFile = open(argv[2], 'w')
      outputFile.write(outputText)
      outputFile.close()


def encrypt(key,text): #encryption of text
   rotateAlphabet=''
   length = len(alphabet)
   for numb in range (0,length): #create shifted alphabet
      rotateAlphabet+=alphabet[(numb+int(key))%length]
   return text.translate(str.maketrans(alphabet, rotateAlphabet)) #translation with table

def decrypt(key,text): #decryption of text
   rotateAlphabet=''
   length = len(alphabet)
   for numb in range (0,length): #create shifted alphabet
      rotateAlphabet+=alphabet[(numb-int(key))%length]
   return text.translate(str.maketrans(alphabet, rotateAlphabet)) #translation with table

if __name__ == "__main__":
   main(sys.argv[1:])
email = "lukas.wuehr@uni-jena.de"
print(email[7]+email[8])