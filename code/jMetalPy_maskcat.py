from jmetal.core.problem import Problem
from jmetal.core.solution import Solution
from code.newfunctions import maskToSolution

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
chromosomesMask = {0:'\0',1:'?l',2:'?u',3:'?d',4:'?h',5:'?H',6:'?s',7:'?a',8:'?b'}

class MaskcatSolution (Solution):
    def __init__(self, number_of_variables: int, number_of_objectives: int, number_of_constraints: int = 0):
        super(MaskcatSolution, self).__init__(number_of_variables, number_of_objectives, number_of_constraints)
        self.number_of_variables = number_of_variables
        self.number_of_objectives = number_of_objectives
        self.number_of_constraints = number_of_constraints
        self.variables = [[] for _ in range(self.number_of_variables)]
        self.objectives = [0.0 for _ in range(self.number_of_objectives)]
        self.constraints = [0.0 for _ in range(self.number_of_constraints)]
        self.attributes = {}

    def __copy__(self):
        new_solution = MaskcatSolution(
            self.number_of_variables,
            self.number_of_objectives)
        new_solution.objectives = self.objectives[:]
        new_solution.variables = self.variables[:]

        new_solution.attributes = self.attributes.copy()
    
    def __eq__(self, solution) -> bool:
        if isinstance(solution, self.__class__):
            return self.variables == solution.variables
        return False

    def __str__(self) -> str:
        return 'Solution(variables={},objectives={},constraints={})'.format(self.variables, self.objectives,
                                                                            self.constraints)

class MaskcatProblem (Problem):

    def __init__ (self, masksList : list):
        super(MaskcatProblem, self).__init__(reference_frot = None)
        
        self.masks = masksList
        self.masksResults = {}

        self.number_of_variables= 7
        self.number_of_objectives= 1
        self.number_of_constraints= 0

        self.directions = [self.MAXIMIZE]
        self.labels = ['Maskcat']

    #-------------- NUEVO ----------------------
    def maskToSolution(self, mask:str):
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

    def solutionToMask(self, solution: MaskcatSolution):
        mask = ''
        for chromosome in solution:
            if chromosome != 0:
                mask = mask + chromosomesMask[chromosome]
        return mask
    #-------------------------------

    def create_solution(self) -> MaskcatSolution:
        """ Creates a random_search solution to the problem.

        :return: Solution. """
        new_solution = MaskcatSolution(self.number_of_variables, self.number_of_objectives)

        new_solution.variables = self.maskToSolution() #Metodo transformar de mascara a array ints -> devuelve lista
        #'?d?d?d?d?d?d' 

        return new_solution

    def evaluate(self, solution: MaskcatSolution) -> MaskcatSolution:
        """ Evaluate a solution. For any new problem inheriting from :class:`Problem`, this method should be
        replaced. Note that this framework ASSUMES minimization, thus solutions must be evaluated in consequence.

        :return: Evaluated solution. """
        score: float
        mask = self.solutionToMask(solution.variables)
        if mask  not in self.masksResults:
            score = execHashcat(mask)
            self.masksResults[mask]=score
        else:
            score = self.masksResults.get(mask)


        solution.objectives[0] =score
        return solution

    def get_name(self) -> str:
        return 'Maskcat'



