import hashlib as hash
import os

def cypherMD5(file):
    fd = open(file, "r", errors='ignore')
    fd2 = open('experiments-file_MD5.txt', 'w')
    fd3 = open('experiments-file_clear.txt', 'w+')

    for line in fd.readlines():
        line.replace("\n","")
        if len(line)>4 and len(line)<=9:
            fd3.write(line)
            hashed = hash.md5(line.encode('utf-8').strip()).hexdigest()
        
            fd2.write(hashed+'\n')

    fd.close()
    fd2.close()
    fd3.close()
    return 0



cypherMD5('shuffled_10-million-password-list-top-1000000.txt')