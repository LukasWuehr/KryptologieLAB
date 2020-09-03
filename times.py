import time, sys
import DES_Pack.desModes as ds
import DES_Pack.generateKey as gk
from RSA_Pack.keyGeneration import keys, saveKeys
from RSA_Pack.rsa import encrypt,key, decrypt
if __name__ == '__main__':
    saveKeys(32, 'pub.txt', 'pvt.txt')
    print('only RSA')
    start = time.time()
    n, e = key('pub.txt')
    encrypt('text.txt', 'RSA_en.txt', n, e)
    n, d = key('pvt.txt')
    decrypt('RSA_en.txt','RSA_de.txt',n,d)
    end = time.time()
    print(end-start)
    print('only DES')
    start = time.time()
    with open('DES_en.txt', 'wb') as file:
        gen = ds.ecb('text.txt', gk.generateKeys(gk.readKey('key.txt')))
        for m in gen:
            file.write(m.to_bytes(16,'big'))
    with open('DES_de.txt', 'wb') as file:
        gen = ds.ecb('DES_en.txt', gk.generateKeys(gk.readKey('key.txt')))
        for m in gen:
            file.write(m.to_bytes(16,'big'))
    end = time.time()
    print(end-start)
    print('RSA and DES')
    start = time.time()
    n, e = key('pub.txt')
    encrypt('key.txt', 'en_key.txt', n, e)
    with open('COMB_en.txt', 'wb') as file:
        gen = ds.ecb('text.txt', gk.generateKeys(gk.readKey('key.txt')))
        for m in gen:
            file.write(m.to_bytes(16, 'big'))

    n, d = key('pvt.txt')
    decrypt('en_key.txt', 'new_key.txt', n, d)
    with open('COMB_de.txt', 'wb') as file:
        gen = ds.ecb('COMB_en.txt', gk.generateKeys(gk.readKey('new_key.txt')))
        for m in gen:
            file.write(m.to_bytes(16, 'big'))
    end = time.time()
    print(end-start)




