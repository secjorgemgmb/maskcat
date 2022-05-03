import hashlib as hash
import os

def cypherMD5(file):
    fd = open(file, "r", errors='ignore')
    fd2 = open('shuffled_top_1M_MD5.txt', 'w')
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



cypherMD5('shuffled_10-million-password-list-top-1000000.txt')