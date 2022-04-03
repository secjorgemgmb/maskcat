import random
import json

from jmetal.core.problem import Problem
from jmetal.core.solution import Solution
# from newfunctions import maskToSolution

from exec import execHashcat


#   l | abcdefghijklmnopqrstuvwxyz [a-z]
#   u | ABCDEFGHIJKLMNOPQRSTUVWXYZ [A-Z]
#   d | 0123456789                 [0-9]
#   h | 0123456789abcdef           [0-9a-f]
#   H | 0123456789ABCDEF           [0-9A-F]
#   s |  !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
#   a | ?l?u?d?s
#   b | 0x00 - 0xff

maskChromosomes=['\0','l','u','d','h','H','s','a','b']
chromosomesMask = {0:'\0',1:'?l',2:'?u',3:'?d',4:'?s',5:'?h',6:'?H',7:'?a',8:'?b'}

# masks_sets = [[3,3,3,3,3,3,0,3],[1,1,1,1,3,3,0,0],[1,1,1,1,1,1,1,0],[2,1,1,1,1,1,3,0],[3,3,1,1,1,1,0,0]]
mask_sets = [
[1, 1, 1, 1, 1, 1, 1, 1], [3, 3, 3, 3, 3, 3, 0, 0], [1, 1, 1, 1, 1, 1, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3], [1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 3, 3], [3, 3, 3, 3, 3, 3, 3, 0], [1, 1, 1, 1, 1, 1, 1, 3], [1, 1, 1, 1, 1, 1, 3, 0], [1, 1, 1, 1, 3, 3, 3, 3], [1, 1, 1, 1, 1, 3, 3, 0], [1, 1, 1, 1, 1, 0, 0, 0], [1, 1, 1, 1, 1, 3, 3, 3], [1, 1, 1, 1, 3, 3, 0, 0], [1, 1, 1, 1, 1, 3, 0, 0], [3, 3, 3, 3, 3, 0, 0, 0], [3, 3, 3, 3, 3, 3, 1, 0], [1, 1, 1, 1, 3, 3, 3, 0], [1, 1, 1, 3, 3, 3, 3, 0], [1, 1, 1, 3, 3, 3, 0, 0], [3, 3, 3, 3, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 3, 3, 3, 3, 0, 0], [1, 3, 3, 3, 3, 3, 3, 0], [1, 1, 3, 3, 3, 3, 3, 3], [3, 3, 1, 1, 1, 1, 0, 0], [3, 3, 3, 3, 3, 3, 1, 1], [2, 2, 2, 2, 2, 2, 2, 0], [3, 3, 3, 3, 3, 3, 3, 1], [2, 1, 1, 1, 1, 1, 3, 3], [2, 1, 1, 1, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0], [3, 3, 3, 3, 1, 1, 1, 1], [1, 3, 3, 3, 3, 3, 3, 3], [3, 1, 3, 1, 3, 1, 0, 0], [1, 1, 1, 3, 3, 3, 3, 3], [3, 3, 1, 1, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1, 1, 0], [2, 2, 2, 2, 2, 2, 0, 0], [3, 3, 1, 1, 1, 1, 1, 0], [3, 3, 3, 0, 0, 0, 0, 0], [3, 1, 1, 1, 1, 1, 1, 1], [3, 3, 3, 1, 1, 1, 0, 0], [3, 3, 3, 3, 1, 1, 0, 0], [2, 1, 1, 1, 3, 3, 3, 3], [2, 1, 1, 1, 1, 1, 1, 3], [3, 3, 3, 3, 1, 1, 1, 0], [2, 2, 2, 2, 2, 2, 2, 2], [3, 3, 3, 3, 3, 1, 0, 0], [3, 1, 1, 1, 1, 1, 1, 0], [2, 1, 1, 1, 1, 3, 3, 3], [1, 3, 3, 3, 3, 3, 0, 0], [1, 1, 3, 3, 3, 3, 3, 0], [3, 1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 1, 1, 4, 0], [1, 1, 1, 3, 3, 1, 1, 1], [1, 1, 1, 1, 3, 0, 0, 0], [3, 3, 3, 1, 1, 1, 1, 1], [1, 1, 1, 3, 3, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 4], [2, 1, 1, 1, 1, 0, 0, 0], [1, 1, 1, 3, 1, 1, 1, 1], [3, 3, 1, 1, 1, 0, 0, 0], [1, 3, 1, 3, 1, 3, 1, 3], [1, 1, 1, 1, 3, 1, 1, 1], [3, 1, 3, 1, 3, 1, 3, 1], [1, 1, 1, 1, 1, 3, 1, 1], [3, 3, 3, 3, 3, 1, 1, 1], [3, 3, 3, 1, 1, 1, 1, 0], [2, 1, 1, 1, 1, 3, 3, 0], [1, 1, 1, 1, 1, 1, 3, 1], [1, 3, 1, 3, 1, 3, 0, 0], [1, 1, 1, 1, 3, 1, 0, 0], [1, 3, 3, 3, 3, 3, 3, 1], [2, 2, 2, 2, 2, 2, 3, 3], [1, 1, 1, 3, 1, 1, 0, 0], [3, 1, 1, 1, 1, 1, 1, 3], [2, 1, 1, 1, 1, 1, 3, 0], [1, 1, 3, 1, 1, 1, 0, 0], [1, 3, 1, 1, 1, 1, 1, 1], [1, 3, 1, 1, 1, 1, 0, 0], [3, 3, 1, 1, 1, 1, 3, 3], [1, 1, 1, 1, 1, 4, 0, 0], [1, 1, 3, 1, 1, 1, 1, 1], [3, 1, 1, 1, 3, 1, 1, 1], [1, 3, 3, 3, 3, 1, 0, 0], [2, 2, 2, 2, 3, 3, 3, 3], [1, 1, 1, 3, 1, 1, 1, 0], [2, 2, 2, 2, 2, 0, 0, 0], [3, 3, 3, 3, 3, 1, 1, 0], [3, 3, 3, 3, 3, 3, 2, 0], [4, 1, 1, 1, 1, 0, 0, 0], [1, 1, 3, 3, 3, 3, 1, 1], [1, 1, 1, 1, 3, 1, 1, 0], [1, 3, 3, 3, 1, 1, 0, 0], [1, 1, 1, 1, 1, 3, 3, 1], [1, 1, 3, 3, 1, 1, 0, 0], [1, 1, 1, 1, 1, 4, 3, 3], [2, 1, 1, 1, 1, 3, 0, 0], [2, 1, 1, 1, 3, 3, 0, 0], [1, 1, 1, 1, 1, 3, 1, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 3, 3, 1, 1], [3, 3, 1, 1, 1, 3, 3, 0], [1, 1, 3, 3, 1, 1, 3, 3], [1, 1, 1, 3, 1, 1, 1, 3], [1, 1, 3, 1, 1, 1, 1, 0], [3, 3, 3, 3, 1, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0], [2, 1, 3, 3, 3, 3, 3, 3], [2, 3, 3, 3, 3, 3, 3, 0], [1, 1, 3, 3, 3, 0, 0, 0], [1, 1, 1, 4, 1, 1, 1, 0], [2, 2, 2, 2, 2, 2, 2, 3], [2, 1, 1, 1, 3, 3, 3, 0], [3, 3, 1, 1, 3, 3, 0, 0], [1, 3, 3, 3, 3, 0, 0, 0], [2, 2, 2, 2, 2, 3, 3, 3], [2, 2, 2, 2, 2, 2, 3, 0], [1, 1, 1, 1, 4, 1, 1, 1], [2, 2, 2, 3, 3, 3, 3, 0], [3, 1, 1, 1, 1, 3, 0, 0], [1, 1, 3, 3, 1, 1, 1, 1], [2, 2, 2, 2, 2, 3, 3, 0], [2, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 3, 3, 1, 0, 0], [1, 3, 1, 1, 1, 1, 1, 0], [1, 3, 3, 1, 3, 3, 0, 0], [2, 2, 2, 2, 3, 3, 0, 0], [1, 1, 1, 3, 3, 3, 1, 1], [1, 1, 1, 1, 4, 3, 3, 0], [1, 1, 1, 1, 1, 1, 4, 3], [1, 1, 1, 4, 1, 1, 1, 1], [3, 3, 0, 0, 0, 0, 0, 0], [1, 3, 1, 1, 3, 1, 0, 0], [3, 3, 3, 3, 3, 3, 4, 0], [2, 2, 2, 2, 0, 0, 0, 0], 
[1, 1, 1, 1, 3, 3, 1, 0], [3, 0, 0, 0, 0, 0, 0, 0], [1, 1, 3, 1, 1, 3, 0, 0], [2, 2, 2, 2, 2, 3, 0, 0], [3, 3, 3, 1, 3, 3, 3, 0], [3, 1, 1, 1, 1, 1, 3, 0], [2, 2, 3, 3, 3, 3, 3, 3], [2, 1, 1, 1, 1, 1, 2, 0], [2, 1, 1, 3, 3, 3, 3, 0], [2, 3, 3, 3, 3, 3, 3, 3], [1, 3, 3, 1, 1, 1, 0, 0], [1, 1, 1, 3, 3, 3, 3, 1], [2, 2, 2, 3, 3, 3, 0, 0], [3, 3, 3, 3, 3, 3, 3, 2], [1, 1, 1, 3, 3, 1, 1, 0], [3, 3, 3, 3, 3, 3, 2, 2], [1, 1, 1, 1, 3, 3, 3, 1], [2, 2, 3, 3, 3, 3, 0, 0], [1, 3, 1, 3, 1, 1, 0, 0], [1, 1, 3, 3, 3, 1, 1, 0], [1, 1, 1, 3, 1, 3, 0, 0], [1, 3, 3, 1, 1, 1, 1, 1], [3, 3, 3, 1, 3, 3, 0, 0], [3, 3, 1, 3, 3, 1, 0, 0], [2, 2, 2, 2, 3, 3, 3, 0], [3, 3, 3, 3, 1, 1, 3, 3], [1, 1, 1, 1, 1, 3, 1, 3], [1, 1, 1, 3, 3, 3, 1, 0], [1, 3, 3, 3, 3, 3, 1, 0], [2, 2, 3, 3, 3, 3, 3, 0], [1, 1, 1, 1, 4, 1, 1, 0], [1, 1, 3, 3, 1, 1, 1, 0], [1, 1, 3, 1, 1, 3, 1, 1], [1, 3, 1, 1, 1, 3, 0, 0], [3, 3, 1, 1, 3, 3, 1, 1], [1, 3, 1, 1, 1, 3, 1, 1], [1, 1, 3, 1, 1, 1, 1, 3], [1, 1, 3, 3, 3, 1, 0, 0], [3, 3, 1, 3, 3, 3, 0, 0], [2, 1, 1, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 1, 3], [1, 1, 1, 1, 1, 4, 3, 0], [1, 1, 1, 1, 3, 1, 1, 3], [1, 1, 1, 1, 1, 4, 1, 1], [1, 1, 3, 1, 3, 1, 0, 0], [2, 1, 1, 0, 0, 0, 0, 0], [3, 1, 1, 1, 3, 1, 0, 0], [2, 1, 1, 3, 3, 3, 0, 0], [1, 1, 1, 1, 4, 3, 3, 3], [3, 1, 3, 1, 1, 1, 0, 0], [3, 1, 1, 3, 1, 1, 0, 0], [3, 3, 3, 1, 1, 3, 3, 3], [1, 1, 1, 1, 1, 4, 1, 0], [3, 3, 3, 3, 1, 3, 0, 0], [3, 1, 1, 1, 1, 0, 0, 0], [1, 1, 1, 3, 0, 0, 0, 0], [1, 1, 1, 4, 3, 3, 3, 3], [1, 1, 4, 1, 1, 1, 1, 1], [1, 3, 1, 1, 1, 1, 3, 1], [2, 2, 2, 0, 0, 0, 0, 0], [3, 1, 3, 3, 3, 3, 0, 0], [1, 3, 1, 1, 1, 1, 1, 3], [3, 1, 1, 1, 1, 1, 3, 3], [1, 1, 1, 1, 1, 1, 4, 1], [1, 3, 1, 3, 1, 1, 1, 1], [3, 1, 1, 1, 3, 3, 0, 0], [1, 1, 3, 3, 3, 1, 1, 1], [1, 1, 1, 1, 3, 1, 3, 1], [1, 1, 1, 4, 3, 3, 0, 0], [1, 3, 1, 1, 3, 1, 1, 1], [1, 1, 3, 1, 1, 1, 3, 1], [1, 3, 3, 3, 1, 3, 3, 3], [3, 3, 4, 3, 3, 4, 3, 3], [4, 0, 0, 0, 0, 0, 0, 0], [1, 1, 4, 1, 1, 1, 1, 0], [3, 3, 1, 1, 3, 3, 3, 3], [1, 4, 1, 1, 1, 1, 1, 0], [1, 1, 1, 3, 1, 1, 3, 1], [1, 1, 3, 1, 3, 1, 1, 1], [2, 1, 1, 1, 1, 2, 0, 0], [1, 1, 1, 3, 1, 3, 1, 1], [1, 1, 3, 1, 3, 1, 3, 1], [3, 3, 1, 3, 3, 3, 3, 0], [3, 1, 1, 1, 1, 3, 1, 1], [1, 4, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 3, 4], [2, 1, 1, 1, 1, 1, 1, 2], [3, 3, 1, 3, 3, 1, 3, 3], [1, 3, 1, 3, 1, 3, 1, 0], [1, 1, 1, 4, 1, 1, 0, 0], [1, 3, 1, 3, 3, 3, 0, 0], [1, 1, 1, 1, 1, 3, 3, 4], [1, 3, 3, 3, 1, 1, 3, 3], [2, 3, 3, 3, 3, 3, 0, 0], [2, 1, 1, 1, 2, 1, 1, 1], [3, 1, 1, 3, 1, 1, 1, 1], [3, 3, 1, 1, 1, 3, 0, 0], [3, 3, 3, 3, 3, 2, 0, 0], [2, 2, 2, 3, 3, 3, 3, 3], [3, 1, 1, 1, 1, 1, 3, 1], [1, 1, 1, 1, 4, 1, 0, 0], [3, 3, 3, 1, 3, 3, 3, 1], [1, 3, 1, 1, 3, 3, 0, 0], [3, 3, 3, 1, 1, 1, 3, 3], [3, 1, 3, 1, 1, 1, 1, 1], [1, 1, 3, 3, 3, 3, 1, 0], [3, 3, 3, 3, 3, 3, 2, 1], [1, 1, 1, 3, 1, 0, 0, 0], [3, 3, 3, 1, 1, 3, 0, 0], [1, 1, 1, 1, 4, 3, 0, 0], [2, 0, 0, 0, 0, 0, 0, 0], [1, 1, 3, 3, 1, 3, 0, 0], [3, 1, 3, 1, 3, 1, 3, 0], [1, 4, 1, 1, 1, 1, 0, 0], [1, 3, 3, 3, 1, 1, 1, 0], [1, 1, 4, 1, 1, 1, 0, 0], [1, 1, 3, 1, 3, 3, 0, 0], [3, 3, 1, 1, 1, 1, 1, 3], [3, 1, 3, 1, 3, 3, 0, 0], [3, 3, 3, 1, 1, 0, 0, 0], [1, 3, 3, 1, 1, 3, 0, 0], [1, 1, 1, 1, 1, 1, 1, 8], [1, 1, 3, 1, 1, 0, 0, 0], [1, 3, 3, 3, 1, 3, 0, 0], [3, 1, 1, 3, 3, 3, 0, 0], [3, 3, 3, 3, 1, 3, 3, 0], [1, 3, 1, 1, 1, 0, 0, 0], [3, 1, 1, 3, 3, 1, 0, 0], [1, 1, 1, 3, 1, 1, 3, 3], [1, 3, 3, 1, 1, 1, 1, 0], [1, 3, 3, 3, 3, 1, 1, 0], [3, 1, 3, 3, 1, 3, 0, 0], [1, 1, 1, 1, 1, 1, 8, 0], [1, 3, 1, 3, 3, 1, 0, 0], [1, 3, 3, 1, 3, 1, 0, 0], [1, 1, 1, 1, 3, 1, 3, 0], [3, 1, 1, 3, 1, 3, 0, 0], [3, 3, 3, 1, 3, 3, 3, 3], [1, 3, 3, 3, 1, 1, 1, 2], [1, 3, 1, 1, 1, 1, 3, 3], [3, 3, 3, 3, 1, 3, 3, 3], [1, 3, 3, 3, 1, 1, 1, 1], [3, 3, 3, 3, 2, 2, 0, 0], [1, 1, 3, 1, 1, 1, 3, 3], [3, 3, 1, 1, 3, 1, 0, 0], [3, 1, 3, 3, 3, 3, 3, 3], [3, 1, 3, 3, 1, 1, 0, 0], [1, 1, 1, 4, 3, 3, 3, 0], [1, 1, 3, 3, 0, 0, 0, 0], [3, 3, 3, 3, 2, 2, 2, 2], [2, 2, 1, 1, 1, 1, 0, 0], [2, 1, 3, 3, 3, 3, 0, 0], [1, 3, 3, 1, 1, 2, 1, 1], 
[1, 1, 1, 1, 3, 1, 3, 3], [3, 1, 1, 1, 3, 3, 3, 3], [3, 3, 1, 1, 1, 3, 3, 3], [3, 3, 3, 1, 3, 1, 0, 0], [3, 1, 3, 1, 1, 3, 0, 0], [3, 2, 1, 1, 1, 1, 1, 1], [1, 3, 1, 3, 1, 3, 1, 1], [3, 3, 1, 3, 1, 3, 0, 0], [1, 1, 1, 1, 1, 1, 1, 2], [3, 3, 3, 3, 3, 3, 3, 4], [1, 1, 1, 3, 1, 1, 3, 0], [3, 1, 3, 3, 3, 1, 0, 0], [3, 3, 1, 3, 1, 1, 0, 0], [1, 1, 3, 3, 1, 3, 1, 1], [1, 1, 1, 1, 4, 0, 0, 0], [1, 1, 3, 3, 1, 1, 1, 3], [2, 1, 1, 1, 1, 3, 1, 1], [1, 3, 1, 1, 1, 1, 3, 0], [3, 3, 3, 3, 2, 1, 1, 1], [3, 3, 1, 1, 3, 3, 3, 0], [1, 3, 1, 1, 3, 1, 1, 0], [2, 3, 1, 1, 1, 1, 1, 1], [3, 3, 3, 3, 1, 1, 1, 3], [3, 1, 1, 1, 0, 0, 0, 0], [1, 3, 3, 3, 3, 1, 1, 1], [3, 1, 1, 1, 1, 3, 3, 0], [3, 3, 3, 3, 3, 3, 8, 8], [1, 1, 3, 1, 1, 1, 3, 0], [1, 3, 1, 1, 3, 1, 3, 1], [1, 1, 1, 1, 1, 2, 0, 0], [4, 1, 1, 1, 1, 1, 1, 0], [3, 1, 1, 1, 1, 3, 1, 0], [1, 1, 3, 0, 0, 0, 0, 0], [3, 3, 1, 3, 3, 3, 3, 3], [2, 3, 3, 3, 3, 3, 3, 1], [3, 3, 3, 3, 3, 1, 3, 3], [3, 3, 3, 3, 1, 1, 3, 0], [2, 3, 3, 3, 3, 3, 3, 2], [1, 3, 3, 1, 3, 3, 3, 3], [3, 3, 3, 3, 2, 2, 2, 0], [1, 1, 1, 3, 3, 1, 1, 3], [1, 1, 1, 1, 1, 1, 2, 0], [1, 1, 1, 1, 1, 1, 4, 4], [1, 3, 1, 1, 1, 3, 1, 0], [3, 3, 2, 1, 1, 1, 1, 1], [3, 3, 3, 3, 3, 1, 3, 0], [3, 3, 3, 4, 3, 3, 3, 0], [3, 1, 1, 3, 1, 1, 3, 1], [2, 2, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 3, 3, 1, 3], [1, 3, 1, 3, 1, 3, 3, 0], [1, 1, 3, 1, 1, 3, 1, 0], [3, 3, 3, 1, 1, 1, 3, 0], [1, 3, 3, 0, 0, 0, 0, 0], [1, 3, 1, 3, 1, 1, 3, 1], [3, 1, 1, 1, 1, 3, 3, 3], [1, 1, 1, 1, 3, 3, 4, 0], [3, 3, 3, 1, 1, 3, 3, 0], [2, 1, 1, 1, 3, 0, 0, 0], [1, 3, 1, 1, 3, 1, 1, 3], [1, 3, 1, 3, 1, 1, 1, 0], [3, 3, 3, 3, 3, 3, 1, 2], [4, 1, 1, 1, 1, 1, 0, 0], [1, 3, 1, 3, 1, 0, 0, 0], [2, 1, 1, 2, 1, 1, 0, 0], [3, 3, 1, 1, 1, 1, 3, 0], [4, 1, 1, 0, 0, 0, 0, 0], [1, 1, 3, 1, 1, 3, 3, 0], [1, 1, 3, 1, 1, 2, 0, 0], [1, 3, 1, 3, 3, 3, 3, 3], [1, 1, 3, 1, 1, 3, 1, 3], [1, 3, 2, 1, 3, 2, 0, 0], [1, 3, 3, 1, 3, 3, 1, 0], [2, 1, 1, 1, 1, 2, 1, 1], [1, 1, 1, 1, 3, 3, 3, 4], [1, 1, 3, 3, 3, 3, 3, 1], [3, 3, 3, 2, 2, 2, 0, 0], [2, 1, 1, 1, 3, 1, 1, 1], [3, 1, 1, 1, 3, 1, 1, 0], [1, 3, 1, 3, 1, 1, 1, 3], [1, 3, 1, 1, 1, 3, 1, 3], [1, 1, 3, 1, 3, 1, 1, 3], [3, 3, 3, 1, 1, 1, 1, 3], [3, 1, 3, 3, 3, 3, 3, 0], [1, 3, 1, 1, 1, 3, 3, 1], [1, 2, 3, 1, 1, 2, 2, 3], [3, 3, 2, 2, 2, 2, 2, 2], [1, 1, 1, 3, 1, 3, 1, 0], [1, 1, 3, 3, 1, 1, 3, 0], [1, 1, 3, 3, 1, 1, 3, 1], [4, 1, 1, 1, 1, 1, 1, 1], [1, 3, 3, 1, 1, 1, 3, 3], [1, 3, 1, 1, 3, 3, 1, 1], [2, 1, 1, 1, 1, 1, 3, 1], [2, 1, 1, 3, 3, 1, 1, 1], [1, 1, 3, 1, 3, 1, 1, 0], [1, 3, 3, 3, 3, 3, 1, 1], [1, 1, 1, 1, 1, 8, 0, 0], [2, 1, 1, 3, 1, 1, 1, 1], [1, 1, 3, 1, 1, 3, 3, 1], [4, 2, 2, 2, 0, 0, 0, 0], [3, 1, 1, 1, 3, 3, 3, 0], [4, 1, 1, 1, 1, 1, 1, 4], [1, 1, 1, 3, 1, 3, 1, 3], [1, 1, 1, 1, 4, 4, 0, 0], [1, 1, 3, 1, 1, 3, 3, 3], [1, 3, 3, 3, 0, 0, 0, 0], [1, 3, 3, 1, 1, 3, 3, 1], [1, 3, 3, 1, 1, 1, 1, 3], [2, 1, 1, 1, 1, 4, 3, 3], [1, 3, 1, 1, 1, 3, 3, 3], [1, 1, 1, 3, 3, 1, 3, 3], [1, 3, 3, 3, 3, 1, 3, 3]
]

masks_experiment = [[4, 3, 4, 1, 3, 3, 4, 2],[1, 1, 1, 2, 2, 2, 4, 1],[3, 3, 4, 4, 0, 0, 1, 2],[1, 3, 1, 1, 4, 0, 3, 1],[3, 4, 4, 2, 2, 3, 4, 4],[3, 1, 4, 3, 0, 4, 0, 3],[2, 2, 4, 3, 4, 1, 4, 1],[2, 2, 3, 2, 4, 4, 3, 4],[4, 3, 1, 2, 4, 1, 3, 4],[2, 1, 4, 3, 4, 3, 3, 4],[3, 1, 1, 1, 4, 3, 2, 1],[1, 3, 2, 1, 0, 0, 2, 0],[3, 2, 3, 4, 4, 1, 3, 1],[3, 2, 3, 1, 2, 4, 3, 4],[3, 3, 4, 3, 0, 0, 0, 3],[4, 2, 3, 3, 4, 2, 2, 3],[3, 1, 1, 2, 2, 2, 2, 3],[3, 2, 2, 3, 4, 1, 2, 0],[3, 1, 3, 3, 0, 0, 1, 4],[4, 3, 4, 2, 1, 4, 4, 0],[4, 2, 1, 1, 0, 0, 1, 2],[4, 1, 4, 3, 0, 3, 2, 0],[2, 3, 4, 3, 3, 4, 2, 1],[1, 1, 4, 4, 2, 3, 1, 0],[2, 2, 1, 3, 3, 4, 3, 2],[1, 4, 4, 1, 1, 1, 4, 4],[3, 3, 3, 2, 4, 1, 2, 1],[2, 3, 2, 1, 1, 0, 3, 0],[1, 2, 3, 3, 1, 2, 2, 3],[3, 1, 1, 2, 3, 1, 1, 3],[4, 2, 3, 2, 3, 1, 4, 4],[2, 1, 4, 1, 1, 0, 3, 4],[4, 1, 1, 1, 1, 2, 2, 4],[3, 4, 4, 1, 1, 3, 2, 1],[1, 2, 3, 3, 2, 2, 1, 1],[2, 2, 3, 3, 3, 4, 3, 0],[2, 4, 2, 4, 3, 2, 1, 2],[1, 1, 3, 3, 0, 1, 4, 2],[4, 3, 4, 3, 3, 4, 3, 1],[3, 3, 4, 3, 1, 1, 2, 2],[2, 1, 1, 3, 4, 3, 0, 0],[1, 1, 3, 3, 1, 1, 1, 4],[2, 4, 3, 3, 0, 2, 1, 4],[3, 4, 4, 3, 3, 0, 3, 2],[2, 1, 3, 3, 3, 4, 0, 4],[4, 2, 4, 1, 4, 4, 2, 0],[4, 3, 4, 1, 2, 2, 2, 3],[1, 1, 3, 2, 3, 1, 3, 2],[1, 4, 1, 1, 0, 4, 4, 2],[4, 2, 2, 3, 0, 2, 4, 0]]

class MaskcatSolution (Solution):
    def __init__(self, number_of_variables: int, number_of_objectives: int, number_of_constraints: int = 0):
        super(MaskcatSolution, self).__init__(number_of_variables, number_of_objectives, number_of_constraints)
        # self.number_of_variables = number_of_variables
        # self.number_of_objectives = number_of_objectives
        # self.number_of_constraints = number_of_constraints
        # self.variables = [[] for _ in range(self.number_of_variables)]
        # self.objectives = [0.0 for _ in range(self.number_of_objectives)]
        # self.constraints = [0.0 for _ in range(self.number_of_constraints)]
        # self.attributes = {}

    def get_number_of_masks(self):
        # try:
        #     return self.variables.index(0)
        # except:
        return self.number_of_variables

    def __copy__(self):
        new_solution = MaskcatSolution(
            self.number_of_variables,
            self.number_of_objectives)
        new_solution.objectives = self.objectives[:]
        new_solution.variables = self.variables[:]

        new_solution.attributes = self.attributes.copy()

        return new_solution
    
    def __eq__(self, solution) -> bool:
        if isinstance(solution, self.__class__):
            return self.variables == solution.variables
        return False

    def __str__(self) -> str:
        return 'Solution(variables={},score={},constraints={})'.format(self.variables, self.objectives,
                                                                            self.constraints)
    
    def getScore(self):
        return self.objectives[0]

    def getMask(self):
        return self.variables

class MaskcatProblem (Problem):

    MINIMIZE = -1
    MAXIMIZE = 1

    def __init__ (self, cache, wordlist_route:str, generation_size:int, pass_len = 7, predefined_masks = 2):
        super(MaskcatProblem, self).__init__()
        
        self.masks = []
        self.cache = cache
        self.masksHistory = []

        self.number_of_variables= pass_len
        self.number_of_objectives= 1
        self.number_of_constraints= 0

        self.number_of_predefined_masks = predefined_masks
        self.number_of_predefined_masks_inserted = 0

        self.wordlist = wordlist_route
        self.generation = 1
        self.generation_counter = 0
        self.generation_size = generation_size

        self.experiment_counter = 0

        self.directions = [self.MAXIMIZE]
        self.labels = ['Maskcat']

    #-------------- MASKS FUNCTIONS ----------------------
    def maskToSolution(self, mask:str):
        mask = mask.replace('?','')
        maskLen = len(mask)

        solution = []
        if maskLen >= self.number_of_variables+1:
            for i in range (maskLen-1):
                solution.append(maskChromosomes.index(mask[i]))
            solution.append(maskChromosomes.index('\0'))
        elif maskLen == self.number_of_variables:
            for i in range (maskLen):
                solution.append(maskChromosomes.index(mask[i]))
            solution.append(maskChromosomes.index('\0'))
        else:
            for i in range (0,self.number_of_variables+1):
                if i < maskLen:
                    solution.append(maskChromosomes.index(mask[i]))
                else:
                    solution.append(maskChromosomes.index('\0'))

        return solution

    def solutionToMask(self, solution: MaskcatSolution):
        mask = ''
        for chromosome in solution:
            if chromosome != 0:
                mask = mask + chromosomesMask[chromosome]
            else:
                return mask
        return mask
    
    def randomMask (self):
        randMask = []
        for i in range (0,self.number_of_variables+1):
            if i < 4:
                chromosome = random.randint(1, 4)
            else:
                chromosome = random.randint(0, 4)
            randMask.append(chromosome)

        # i = 0 
        # while i != 1:
        #     if randMask[i] == 0:
        #         print(randMask)
        #         randMask[i] = random.randint(0, 4)
        #         i = i-1
        #     i = i+1

        # if 0 not in randMask:
        #     randMask[7]=0
        return randMask
        # return masks_sets[random.randint(0,4)]
    
    #-------------------------------

    def create_solution(self) -> MaskcatSolution:
        """ Creates a random_search solution to the problem.

        :return: Solution. """

        #Mascara alatoria a partir del charset de arriba
        new_solution = MaskcatSolution(self.number_of_variables, self.number_of_objectives)

        if self.number_of_predefined_masks_inserted != self.number_of_predefined_masks:
            # predefined_mask = mask_sets[random.randint(0, len(mask_sets))]
            # while len(predefined_mask) != self.number_of_variables+1 and not(len(predefined_mask)>self.number_of_variables):
            #     predefined_mask.append(0)

            predefined_mask = masks_experiment[self.experiment_counter]
            self.experiment_counter += 1

            new_solution.variables = predefined_mask
            self.number_of_predefined_masks_inserted = self.number_of_predefined_masks_inserted + 1
        else:
            new_solution.variables = self.randomMask()
        # new_solution.variables = self.maskToSolution() #Metodo transformar de mascara a array ints -> devuelve lista
        # #'?d?d?d?d?d?d' 

        return new_solution

    def evaluate(self, solution: MaskcatSolution) -> MaskcatSolution:
        score: float

        self.generation_counter = self.generation_counter + 1

        mask = self.solutionToMask(solution.variables)

        if len(mask)>=8: # 4 ?x o más
            if mask  not in self.cache:
                print("Evaluating: {}".format(mask))
                execution = execHashcat(self.wordlist, mask)
                score = execution[0]
                time = execution[1]
                self.cache[mask]={"Score":score,"Time":time} 
            else:
                score = self.cache.get(mask)["Score"]
        else:
            score = -0.0

        self.masksHistory.append([solution.variables, mask, score, self.generation])
        solution.objectives[0] =score

        if self.generation_counter == self.generation_size:
            self.generation = self.generation + 1
            self.generation_counter = 0

        return solution
    def get_name(self) -> str:
        return 'Maskcat'

    def get_cache(self):
        return self.cache

    def get_masksHistory(self):
        return self.masksHistory


