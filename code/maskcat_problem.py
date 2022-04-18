import random
import copy

from jmetal.core.problem import Problem
from jmetal.core.solution import Solution


from exec import HashcatExecution


#   l | abcdefghijklmnopqrstuvwxyz [a-z]
#   u | ABCDEFGHIJKLMNOPQRSTUVWXYZ [A-Z]
#   d | 0123456789                 [0-9]
#   h | 0123456789abcdef           [0-9a-f]
#   H | 0123456789ABCDEF           [0-9A-F]
#   s |  !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
#   a | ?l?u?d?s
#   b | 0x00 - 0xff

MASK_GENS=['\0','l','u','d','h','H','s','a','b']
GENS_MASK = {0:'\0',1:'?l',2:'?u',3:'?d',4:'?s',5:'?h',6:'?H',7:'?a',8:'?b'}

# masks_sets = [[3,3,3,3,3,3,0,3],[1,1,1,1,3,3,0,0],[1,1,1,1,1,1,1,0],[2,1,1,1,1,1,3,0],[3,3,1,1,1,1,0,0]]
MASK_SETS = [
[1, 1, 1, 1, 1, 1, 1, 1], [3, 3, 3, 3, 3, 3, 0, 0], [1, 1, 1, 1, 1, 1, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3], [1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 3, 3], [3, 3, 3, 3, 3, 3, 3, 0], [1, 1, 1, 1, 1, 1, 1, 3], [1, 1, 1, 1, 1, 1, 3, 0], [1, 1, 1, 1, 3, 3, 3, 3], [1, 1, 1, 1, 1, 3, 3, 0], [1, 1, 1, 1, 1, 0, 0, 0], [1, 1, 1, 1, 1, 3, 3, 3], [1, 1, 1, 1, 3, 3, 0, 0], [1, 1, 1, 1, 1, 3, 0, 0], [3, 3, 3, 3, 3, 0, 0, 0], [3, 3, 3, 3, 3, 3, 1, 0], [1, 1, 1, 1, 3, 3, 3, 0], [1, 1, 1, 3, 3, 3, 3, 0], [1, 1, 1, 3, 3, 3, 0, 0], [3, 3, 3, 3, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 3, 3, 3, 3, 0, 0], [1, 3, 3, 3, 3, 3, 3, 0], [1, 1, 3, 3, 3, 3, 3, 3], [3, 3, 1, 1, 1, 1, 0, 0], [3, 3, 3, 3, 3, 3, 1, 1], [2, 2, 2, 2, 2, 2, 2, 0], [3, 3, 3, 3, 3, 3, 3, 1], [2, 1, 1, 1, 1, 1, 3, 3], [2, 1, 1, 1, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0], [3, 3, 3, 3, 1, 1, 1, 1], [1, 3, 3, 3, 3, 3, 3, 3], [3, 1, 3, 1, 3, 1, 0, 0], [1, 1, 1, 3, 3, 3, 3, 3], [3, 3, 1, 1, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1, 1, 0], [2, 2, 2, 2, 2, 2, 0, 0], [3, 3, 1, 1, 1, 1, 1, 0], [3, 3, 3, 0, 0, 0, 0, 0], [3, 1, 1, 1, 1, 1, 1, 1], [3, 3, 3, 1, 1, 1, 0, 0], [3, 3, 3, 3, 1, 1, 0, 0], [2, 1, 1, 1, 3, 3, 3, 3], [2, 1, 1, 1, 1, 1, 1, 3], [3, 3, 3, 3, 1, 1, 1, 0], [2, 2, 2, 2, 2, 2, 2, 2], [3, 3, 3, 3, 3, 1, 0, 0], [3, 1, 1, 1, 1, 1, 1, 0], [2, 1, 1, 1, 1, 3, 3, 3], [1, 3, 3, 3, 3, 3, 0, 0], [1, 1, 3, 3, 3, 3, 3, 0], [3, 1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 1, 1, 4, 0], [1, 1, 1, 3, 3, 1, 1, 1], [1, 1, 1, 1, 3, 0, 0, 0], [3, 3, 3, 1, 1, 1, 1, 1], [1, 1, 1, 3, 3, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 4], [2, 1, 1, 1, 1, 0, 0, 0], [1, 1, 1, 3, 1, 1, 1, 1], [3, 3, 1, 1, 1, 0, 0, 0], [1, 3, 1, 3, 1, 3, 1, 3], [1, 1, 1, 1, 3, 1, 1, 1], [3, 1, 3, 1, 3, 1, 3, 1], [1, 1, 1, 1, 1, 3, 1, 1], [3, 3, 3, 3, 3, 1, 1, 1], [3, 3, 3, 1, 1, 1, 1, 0], [2, 1, 1, 1, 1, 3, 3, 0], [1, 1, 1, 1, 1, 1, 3, 1], [1, 3, 1, 3, 1, 3, 0, 0], [1, 1, 1, 1, 3, 1, 0, 0], [1, 3, 3, 3, 3, 3, 3, 1], [2, 2, 2, 2, 2, 2, 3, 3], [1, 1, 1, 3, 1, 1, 0, 0], [3, 1, 1, 1, 1, 1, 1, 3], [2, 1, 1, 1, 1, 1, 3, 0], [1, 1, 3, 1, 1, 1, 0, 0], [1, 3, 1, 1, 1, 1, 1, 1], [1, 3, 1, 1, 1, 1, 0, 0], [3, 3, 1, 1, 1, 1, 3, 3], [1, 1, 1, 1, 1, 4, 0, 0], [1, 1, 3, 1, 1, 1, 1, 1], [3, 1, 1, 1, 3, 1, 1, 1], [1, 3, 3, 3, 3, 1, 0, 0], [2, 2, 2, 2, 3, 3, 3, 3], [1, 1, 1, 3, 1, 1, 1, 0], [2, 2, 2, 2, 2, 0, 0, 0], [3, 3, 3, 3, 3, 1, 1, 0], [3, 3, 3, 3, 3, 3, 2, 0], [4, 1, 1, 1, 1, 0, 0, 0], [1, 1, 3, 3, 3, 3, 1, 1], [1, 1, 1, 1, 3, 1, 1, 0], [1, 3, 3, 3, 1, 1, 0, 0], [1, 1, 1, 1, 1, 3, 3, 1], [1, 1, 3, 3, 1, 1, 0, 0], [1, 1, 1, 1, 1, 4, 3, 3], [2, 1, 1, 1, 1, 3, 0, 0], [2, 1, 1, 1, 3, 3, 0, 0], [1, 1, 1, 1, 1, 3, 1, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 3, 3, 1, 1], [3, 3, 1, 1, 1, 3, 3, 0], [1, 1, 3, 3, 1, 1, 3, 3], [1, 1, 1, 3, 1, 1, 1, 3], [1, 1, 3, 1, 1, 1, 1, 0], [3, 3, 3, 3, 1, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0], [2, 1, 3, 3, 3, 3, 3, 3], [2, 3, 3, 3, 3, 3, 3, 0], [1, 1, 3, 3, 3, 0, 0, 0], [1, 1, 1, 4, 1, 1, 1, 0], [2, 2, 2, 2, 2, 2, 2, 3], [2, 1, 1, 1, 3, 3, 3, 0], [3, 3, 1, 1, 3, 3, 0, 0], [1, 3, 3, 3, 3, 0, 0, 0], [2, 2, 2, 2, 2, 3, 3, 3], [2, 2, 2, 2, 2, 2, 3, 0], [1, 1, 1, 1, 4, 1, 1, 1], [2, 2, 2, 3, 3, 3, 3, 0], [3, 1, 1, 1, 1, 3, 0, 0], [1, 1, 3, 3, 1, 1, 1, 1], [2, 2, 2, 2, 2, 3, 3, 0], [2, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 3, 3, 1, 0, 0], [1, 3, 1, 1, 1, 1, 1, 0], [1, 3, 3, 1, 3, 3, 0, 0], [2, 2, 2, 2, 3, 3, 0, 0], [1, 1, 1, 3, 3, 3, 1, 1], [1, 1, 1, 1, 4, 3, 3, 0], [1, 1, 1, 1, 1, 1, 4, 3], [1, 1, 1, 4, 1, 1, 1, 1], [3, 3, 0, 0, 0, 0, 0, 0], [1, 3, 1, 1, 3, 1, 0, 0], [3, 3, 3, 3, 3, 3, 4, 0], [2, 2, 2, 2, 0, 0, 0, 0], 
[1, 1, 1, 1, 3, 3, 1, 0], [3, 0, 0, 0, 0, 0, 0, 0], [1, 1, 3, 1, 1, 3, 0, 0], [2, 2, 2, 2, 2, 3, 0, 0], [3, 3, 3, 1, 3, 3, 3, 0], [3, 1, 1, 1, 1, 1, 3, 0], [2, 2, 3, 3, 3, 3, 3, 3], [2, 1, 1, 1, 1, 1, 2, 0], [2, 1, 1, 3, 3, 3, 3, 0], [2, 3, 3, 3, 3, 3, 3, 3], [1, 3, 3, 1, 1, 1, 0, 0], [1, 1, 1, 3, 3, 3, 3, 1], [2, 2, 2, 3, 3, 3, 0, 0], [3, 3, 3, 3, 3, 3, 3, 2], [1, 1, 1, 3, 3, 1, 1, 0], [3, 3, 3, 3, 3, 3, 2, 2], [1, 1, 1, 1, 3, 3, 3, 1], [2, 2, 3, 3, 3, 3, 0, 0], [1, 3, 1, 3, 1, 1, 0, 0], [1, 1, 3, 3, 3, 1, 1, 0], [1, 1, 1, 3, 1, 3, 0, 0], [1, 3, 3, 1, 1, 1, 1, 1], [3, 3, 3, 1, 3, 3, 0, 0], [3, 3, 1, 3, 3, 1, 0, 0], [2, 2, 2, 2, 3, 3, 3, 0], [3, 3, 3, 3, 1, 1, 3, 3], [1, 1, 1, 1, 1, 3, 1, 3], [1, 1, 1, 3, 3, 3, 1, 0], [1, 3, 3, 3, 3, 3, 1, 0], [2, 2, 3, 3, 3, 3, 3, 0], [1, 1, 1, 1, 4, 1, 1, 0], [1, 1, 3, 3, 1, 1, 1, 0], [1, 1, 3, 1, 1, 3, 1, 1], [1, 3, 1, 1, 1, 3, 0, 0], [3, 3, 1, 1, 3, 3, 1, 1], [1, 3, 1, 1, 1, 3, 1, 1], [1, 1, 3, 1, 1, 1, 1, 3], [1, 1, 3, 3, 3, 1, 0, 0], [3, 3, 1, 3, 3, 3, 0, 0], [2, 1, 1, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 1, 3], [1, 1, 1, 1, 1, 4, 3, 0], [1, 1, 1, 1, 3, 1, 1, 3], [1, 1, 1, 1, 1, 4, 1, 1], [1, 1, 3, 1, 3, 1, 0, 0], [2, 1, 1, 0, 0, 0, 0, 0], [3, 1, 1, 1, 3, 1, 0, 0], [2, 1, 1, 3, 3, 3, 0, 0], [1, 1, 1, 1, 4, 3, 3, 3], [3, 1, 3, 1, 1, 1, 0, 0], [3, 1, 1, 3, 1, 1, 0, 0], [3, 3, 3, 1, 1, 3, 3, 3], [1, 1, 1, 1, 1, 4, 1, 0], [3, 3, 3, 3, 1, 3, 0, 0], [3, 1, 1, 1, 1, 0, 0, 0], [1, 1, 1, 3, 0, 0, 0, 0], [1, 1, 1, 4, 3, 3, 3, 3], [1, 1, 4, 1, 1, 1, 1, 1], [1, 3, 1, 1, 1, 1, 3, 1], [2, 2, 2, 0, 0, 0, 0, 0], [3, 1, 3, 3, 3, 3, 0, 0], [1, 3, 1, 1, 1, 1, 1, 3], [3, 1, 1, 1, 1, 1, 3, 3], [1, 1, 1, 1, 1, 1, 4, 1], [1, 3, 1, 3, 1, 1, 1, 1], [3, 1, 1, 1, 3, 3, 0, 0], [1, 1, 3, 3, 3, 1, 1, 1], [1, 1, 1, 1, 3, 1, 3, 1], [1, 1, 1, 4, 3, 3, 0, 0], [1, 3, 1, 1, 3, 1, 1, 1], [1, 1, 3, 1, 1, 1, 3, 1], [1, 3, 3, 3, 1, 3, 3, 3], [3, 3, 4, 3, 3, 4, 3, 3], [4, 0, 0, 0, 0, 0, 0, 0], [1, 1, 4, 1, 1, 1, 1, 0], [3, 3, 1, 1, 3, 3, 3, 3], [1, 4, 1, 1, 1, 1, 1, 0], [1, 1, 1, 3, 1, 1, 3, 1], [1, 1, 3, 1, 3, 1, 1, 1], [2, 1, 1, 1, 1, 2, 0, 0], [1, 1, 1, 3, 1, 3, 1, 1], [1, 1, 3, 1, 3, 1, 3, 1], [3, 3, 1, 3, 3, 3, 3, 0], [3, 1, 1, 1, 1, 3, 1, 1], [1, 4, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 3, 4], [2, 1, 1, 1, 1, 1, 1, 2], [3, 3, 1, 3, 3, 1, 3, 3], [1, 3, 1, 3, 1, 3, 1, 0], [1, 1, 1, 4, 1, 1, 0, 0], [1, 3, 1, 3, 3, 3, 0, 0], [1, 1, 1, 1, 1, 3, 3, 4], [1, 3, 3, 3, 1, 1, 3, 3], [2, 3, 3, 3, 3, 3, 0, 0], [2, 1, 1, 1, 2, 1, 1, 1], [3, 1, 1, 3, 1, 1, 1, 1], [3, 3, 1, 1, 1, 3, 0, 0], [3, 3, 3, 3, 3, 2, 0, 0], [2, 2, 2, 3, 3, 3, 3, 3], [3, 1, 1, 1, 1, 1, 3, 1], [1, 1, 1, 1, 4, 1, 0, 0], [3, 3, 3, 1, 3, 3, 3, 1], [1, 3, 1, 1, 3, 3, 0, 0], [3, 3, 3, 1, 1, 1, 3, 3], [3, 1, 3, 1, 1, 1, 1, 1], [1, 1, 3, 3, 3, 3, 1, 0], [3, 3, 3, 3, 3, 3, 2, 1], [1, 1, 1, 3, 1, 0, 0, 0], [3, 3, 3, 1, 1, 3, 0, 0], [1, 1, 1, 1, 4, 3, 0, 0], [2, 0, 0, 0, 0, 0, 0, 0], [1, 1, 3, 3, 1, 3, 0, 0], [3, 1, 3, 1, 3, 1, 3, 0], [1, 4, 1, 1, 1, 1, 0, 0], [1, 3, 3, 3, 1, 1, 1, 0], [1, 1, 4, 1, 1, 1, 0, 0], [1, 1, 3, 1, 3, 3, 0, 0], [3, 3, 1, 1, 1, 1, 1, 3], [3, 1, 3, 1, 3, 3, 0, 0], [3, 3, 3, 1, 1, 0, 0, 0], [1, 3, 3, 1, 1, 3, 0, 0], [1, 1, 1, 1, 1, 1, 1, 8], [1, 1, 3, 1, 1, 0, 0, 0], [1, 3, 3, 3, 1, 3, 0, 0], [3, 1, 1, 3, 3, 3, 0, 0], [3, 3, 3, 3, 1, 3, 3, 0], [1, 3, 1, 1, 1, 0, 0, 0], [3, 1, 1, 3, 3, 1, 0, 0], [1, 1, 1, 3, 1, 1, 3, 3], [1, 3, 3, 1, 1, 1, 1, 0], [1, 3, 3, 3, 3, 1, 1, 0], [3, 1, 3, 3, 1, 3, 0, 0], [1, 1, 1, 1, 1, 1, 8, 0], [1, 3, 1, 3, 3, 1, 0, 0], [1, 3, 3, 1, 3, 1, 0, 0], [1, 1, 1, 1, 3, 1, 3, 0], [3, 1, 1, 3, 1, 3, 0, 0], [3, 3, 3, 1, 3, 3, 3, 3], [1, 3, 3, 3, 1, 1, 1, 2], [1, 3, 1, 1, 1, 1, 3, 3], [3, 3, 3, 3, 1, 3, 3, 3], [1, 3, 3, 3, 1, 1, 1, 1], [3, 3, 3, 3, 2, 2, 0, 0], [1, 1, 3, 1, 1, 1, 3, 3], [3, 3, 1, 1, 3, 1, 0, 0], [3, 1, 3, 3, 3, 3, 3, 3], [3, 1, 3, 3, 1, 1, 0, 0], [1, 1, 1, 4, 3, 3, 3, 0], [1, 1, 3, 3, 0, 0, 0, 0], [3, 3, 3, 3, 2, 2, 2, 2], [2, 2, 1, 1, 1, 1, 0, 0], [2, 1, 3, 3, 3, 3, 0, 0], [1, 3, 3, 1, 1, 2, 1, 1], 
[1, 1, 1, 1, 3, 1, 3, 3], [3, 1, 1, 1, 3, 3, 3, 3], [3, 3, 1, 1, 1, 3, 3, 3], [3, 3, 3, 1, 3, 1, 0, 0], [3, 1, 3, 1, 1, 3, 0, 0], [3, 2, 1, 1, 1, 1, 1, 1], [1, 3, 1, 3, 1, 3, 1, 1], [3, 3, 1, 3, 1, 3, 0, 0], [1, 1, 1, 1, 1, 1, 1, 2], [3, 3, 3, 3, 3, 3, 3, 4], [1, 1, 1, 3, 1, 1, 3, 0], [3, 1, 3, 3, 3, 1, 0, 0], [3, 3, 1, 3, 1, 1, 0, 0], [1, 1, 3, 3, 1, 3, 1, 1], [1, 1, 1, 1, 4, 0, 0, 0], [1, 1, 3, 3, 1, 1, 1, 3], [2, 1, 1, 1, 1, 3, 1, 1], [1, 3, 1, 1, 1, 1, 3, 0], [3, 3, 3, 3, 2, 1, 1, 1], [3, 3, 1, 1, 3, 3, 3, 0], [1, 3, 1, 1, 3, 1, 1, 0], [2, 3, 1, 1, 1, 1, 1, 1], [3, 3, 3, 3, 1, 1, 1, 3], [3, 1, 1, 1, 0, 0, 0, 0], [1, 3, 3, 3, 3, 1, 1, 1], [3, 1, 1, 1, 1, 3, 3, 0], [3, 3, 3, 3, 3, 3, 8, 8], [1, 1, 3, 1, 1, 1, 3, 0], [1, 3, 1, 1, 3, 1, 3, 1], [1, 1, 1, 1, 1, 2, 0, 0], [4, 1, 1, 1, 1, 1, 1, 0], [3, 1, 1, 1, 1, 3, 1, 0], [1, 1, 3, 0, 0, 0, 0, 0], [3, 3, 1, 3, 3, 3, 3, 3], [2, 3, 3, 3, 3, 3, 3, 1], [3, 3, 3, 3, 3, 1, 3, 3], [3, 3, 3, 3, 1, 1, 3, 0], [2, 3, 3, 3, 3, 3, 3, 2], [1, 3, 3, 1, 3, 3, 3, 3], [3, 3, 3, 3, 2, 2, 2, 0], [1, 1, 1, 3, 3, 1, 1, 3], [1, 1, 1, 1, 1, 1, 2, 0], [1, 1, 1, 1, 1, 1, 4, 4], [1, 3, 1, 1, 1, 3, 1, 0], [3, 3, 2, 1, 1, 1, 1, 1], [3, 3, 3, 3, 3, 1, 3, 0], [3, 3, 3, 4, 3, 3, 3, 0], [3, 1, 1, 3, 1, 1, 3, 1], [2, 2, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 3, 3, 1, 3], [1, 3, 1, 3, 1, 3, 3, 0], [1, 1, 3, 1, 1, 3, 1, 0], [3, 3, 3, 1, 1, 1, 3, 0], [1, 3, 3, 0, 0, 0, 0, 0], [1, 3, 1, 3, 1, 1, 3, 1], [3, 1, 1, 1, 1, 3, 3, 3], [1, 1, 1, 1, 3, 3, 4, 0], [3, 3, 3, 1, 1, 3, 3, 0], [2, 1, 1, 1, 3, 0, 0, 0], [1, 3, 1, 1, 3, 1, 1, 3], [1, 3, 1, 3, 1, 1, 1, 0], [3, 3, 3, 3, 3, 3, 1, 2], [4, 1, 1, 1, 1, 1, 0, 0], [1, 3, 1, 3, 1, 0, 0, 0], [2, 1, 1, 2, 1, 1, 0, 0], [3, 3, 1, 1, 1, 1, 3, 0], [4, 1, 1, 0, 0, 0, 0, 0], [1, 1, 3, 1, 1, 3, 3, 0], [1, 1, 3, 1, 1, 2, 0, 0], [1, 3, 1, 3, 3, 3, 3, 3], [1, 1, 3, 1, 1, 3, 1, 3], [1, 3, 2, 1, 3, 2, 0, 0], [1, 3, 3, 1, 3, 3, 1, 0], [2, 1, 1, 1, 1, 2, 1, 1], [1, 1, 1, 1, 3, 3, 3, 4], [1, 1, 3, 3, 3, 3, 3, 1], [3, 3, 3, 2, 2, 2, 0, 0], [2, 1, 1, 1, 3, 1, 1, 1], [3, 1, 1, 1, 3, 1, 1, 0], [1, 3, 1, 3, 1, 1, 1, 3], [1, 3, 1, 1, 1, 3, 1, 3], [1, 1, 3, 1, 3, 1, 1, 3], [3, 3, 3, 1, 1, 1, 1, 3], [3, 1, 3, 3, 3, 3, 3, 0], [1, 3, 1, 1, 1, 3, 3, 1], [1, 2, 3, 1, 1, 2, 2, 3], [3, 3, 2, 2, 2, 2, 2, 2], [1, 1, 1, 3, 1, 3, 1, 0], [1, 1, 3, 3, 1, 1, 3, 0], [1, 1, 3, 3, 1, 1, 3, 1], [4, 1, 1, 1, 1, 1, 1, 1], [1, 3, 3, 1, 1, 1, 3, 3], [1, 3, 1, 1, 3, 3, 1, 1], [2, 1, 1, 1, 1, 1, 3, 1], [2, 1, 1, 3, 3, 1, 1, 1], [1, 1, 3, 1, 3, 1, 1, 0], [1, 3, 3, 3, 3, 3, 1, 1], [1, 1, 1, 1, 1, 8, 0, 0], [2, 1, 1, 3, 1, 1, 1, 1], [1, 1, 3, 1, 1, 3, 3, 1], [4, 2, 2, 2, 0, 0, 0, 0], [3, 1, 1, 1, 3, 3, 3, 0], [4, 1, 1, 1, 1, 1, 1, 4], [1, 1, 1, 3, 1, 3, 1, 3], [1, 1, 1, 1, 4, 4, 0, 0], [1, 1, 3, 1, 1, 3, 3, 3], [1, 3, 3, 3, 0, 0, 0, 0], [1, 3, 3, 1, 1, 3, 3, 1], [1, 3, 3, 1, 1, 1, 1, 3], [2, 1, 1, 1, 1, 4, 3, 3], [1, 3, 1, 1, 1, 3, 3, 3], [1, 1, 1, 3, 3, 1, 3, 3], [1, 3, 3, 3, 3, 1, 3, 3]
]

class MaskcatSolution (Solution):
    def __init__(self, number_of_variables: int, number_of_objectives: int, number_of_constraints: int = 0):
        super(MaskcatSolution, self).__init__(number_of_variables, number_of_objectives, number_of_constraints)

    def get_number_of_masks(self):
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
    
    def get_score(self):
        return self.objectives[0]

    def get_mask(self):
        return self.variables

class MaskcatProblem (Problem):

    MINIMIZE = -1
    MAXIMIZE = 1

    def __init__ (self, cache, wordlist_route:str, generation_size:int,  OS:str, pass_len = 7, predefined_masks = 2):
        super(MaskcatProblem, self).__init__()
        
        self.masks = []
        self.cache = cache
        self.masks_history = []
        self.executioner = HashcatExecution(OS)


        self.number_of_variables= pass_len
        self.number_of_objectives= 1
        self.number_of_constraints= 0

        self.number_of_predefined_masks = predefined_masks
        self.number_of_predefined_masks_inserted = 0

        self.wordlist = wordlist_route
        self.generation = 1
        self.generation_counter = 0
        self.generation_size = generation_size

        self.directions = [self.MAXIMIZE]
        self.labels = ['Maskcat']

    def mask_to_solution(self, mask:str):
        mask = mask.replace('?','')
        mask_len = len(mask)

        solution = []
        if mask_len >= self.number_of_variables+1:
            for i in range (mask_len-1):
                solution.append(MASK_GENS.index(mask[i]))
            solution.append(MASK_GENS.index('\0'))
        elif mask_len == self.number_of_variables:
            for i in range (mask_len):
                solution.append(MASK_GENS.index(mask[i]))
            solution.append(MASK_GENS.index('\0'))
        else:
            for i in range (0,self.number_of_variables+1):
                if i < mask_len:
                    solution.append(MASK_GENS.index(mask[i]))
                else:
                    solution.append(MASK_GENS.index('\0'))

        return solution

    def solution_to_mask(self, solution: MaskcatSolution):
        mask = ''
        for chromosome in solution:
            if chromosome != 0:
                mask = mask + GENS_MASK[chromosome]
            else:
                return mask
        return mask
    
    def random_mask (self):
        rand_mask = []
        for i in range (0,self.number_of_variables+1):
            if i < 4:
                chromosome = random.randint(1, 4)
            else:
                chromosome = random.randint(0, 4)
            rand_mask.append(chromosome)

        return rand_mask

    def create_solution(self) -> MaskcatSolution:
        new_solution = MaskcatSolution(self.number_of_variables, self.number_of_objectives)

        if self.number_of_predefined_masks_inserted != self.number_of_predefined_masks:
            predefined_mask = copy.copy(MASK_SETS[random.randint(0, len(MASK_SETS))])
            while len(predefined_mask) != self.number_of_variables+1 and not(len(predefined_mask)>self.number_of_variables):
                predefined_mask.append(0)

            new_solution.variables = predefined_mask
            self.number_of_predefined_masks_inserted = self.number_of_predefined_masks_inserted + 1
        else:
            new_solution.variables = self.random_mask()

        return new_solution

    def evaluate(self, solution: MaskcatSolution) -> MaskcatSolution:
        score: float

        self.generation_counter = self.generation_counter + 1

        mask = self.solution_to_mask(solution.variables)

        if len(mask)>=8: # 4 ?x o más
            if mask  not in self.cache:
                execution = self.executioner.run(self.wordlist, mask)
                score = execution[0]
                time = execution[1]
                self.cache[mask]={"Score":score,"Time":time} 
            else:
                score = self.cache.get(mask)["Score"]
        else:
            score = -0.0

        self.masks_history.append([solution.variables, mask, score, self.generation])
        solution.objectives[0] =score

        if self.generation_counter == self.generation_size:
            self.generation = self.generation + 1
            self.generation_counter = 0

        return solution

    def get_name(self) -> str:
        return 'Maskcat'

    def get_cache(self):
        return self.cache

    def get_masks_history(self):
        return self.masks_history


