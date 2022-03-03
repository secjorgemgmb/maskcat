from numpy import array_equal


maskChromosomes=['\0','l','u','d','h','H','s','a','b']
chromosomesMask = {0:'\0',1:'?l',2:'?u',3:'?d',4:'?s',5:'?h',6:'?H',7:'?a',8:'?b'}

def formatLen(array):
    size = len(array)
    if size != 8:
        for i in range (size, 8):
            array.append(0)
    return array


file1 = open("kaonashi.hcmask", 'r')
file2 = open("kaonashi_array.txt", "w")

Lines = file1.readlines()

print(Lines)

masks = list(chromosomesMask.values())
arrayLines = []
arrayMask = []
n  = 2
for line in Lines:

    line = line.replace("\n", "")
    if len(line)<17:
        for index in range(0, len(line), n):
            arrayMask.append(masks.index(line[index : index + n]))
        arrayMask = formatLen(arrayMask)
        arrayLines.append(str(arrayMask))
    arrayMask=[]

print("[")
for array in arrayLines:
    print(str(array)+", ")
print("]")

file2.writelines(arrayLines)

file1.close()
file2.close()

