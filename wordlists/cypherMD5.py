import hashlib as hash
import os

def cypherMD5(file):
    fd = open(file, "r", errors='ignore')
    fd2 = open('/Users/jorgemartinezgarcia/CiberSeg utils/rockyouMD5.txt', 'w')
    do = True

    while do:
        readed = fd.readline()

        if readed == '':
            do = False
        #print('\n')
        hashed = hash.md5(readed.encode('utf-8').strip()).hexdigest()
        
        fd2.write(hashed+'\n')

    fd.close()
    fd2.close()
    return 0



cypherMD5('/Users/jorgemartinezgarcia/CiberSeg utils/rockyou.txt')