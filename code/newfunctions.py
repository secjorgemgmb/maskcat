import random


maskChromosomes=['\0','l','u','d','h','H','s','a','b']
chromosomesMask = {0:'\0',1:'?l',2:'?u',3:'?d',4:'?h',5:'?H',6:'?s',7:'?a',8:'?b'}

def maskToSolution(mask:str):
    mask = mask.replace('?','')
    maskLen = len(mask)

    solution = []
    if maskLen >= 8:
        for i in range (maskLen-1):
            solution.append(maskChromosomes.index(mask[i]))
        solution.append(maskChromosomes.index('\0'))
    elif maskLen == 7:
        for i in range (maskLen):
            solution.append(maskChromosomes.index(mask[i]))
        solution.append(maskChromosomes.index('\0'))
    else:
        for i in range (0,8):
            if i < maskLen:
                solution.append(maskChromosomes.index(mask[i]))
            else:
                solution.append(maskChromosomes.index('\0'))

    return solution

def solutionToMask (solution:list):
    mask = ''
    for chromosome in solution:
        if chromosome != 0:
            mask = mask + chromosomesMask[chromosome]
    return mask

def randomMask ():
    randMask = []
    for i in range (0,8):
        chromosome = random.randint(0, 8)
        randMask.append(chromosome)
    return randMask



solution = randomMask()
print('solution = '+str(solution))
mask = solutionToMask(solution)
print('mask = '+ mask)
