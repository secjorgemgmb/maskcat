import hashlib as hash
import os

def cypherMD5(file):
    fd = open(file, "r", errors='ignore')
    fd2 = open('shuffled_hashes_MD5.txt', 'w')

    for line in fd.readlines():
        if len(line)<=8:
            hashed = hash.md5(line.encode('utf-8').strip()).hexdigest()
        
            fd2.write(hashed+'\n')

    fd.close()
    fd2.close()
    return 0



cypherMD5('shuffled_10-million-password-list-top-1000000.txt')