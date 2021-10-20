from jmetal.core.problem import Problem
from jmetal.core.solution import Solution

from exec import execHashcat

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
        self.masksResults = {
            'masksList' : [],
            'punctuations': []
        }

        self.number_of_variables= len(self.masks)
        self.number_of_objectives= 1
        self.number_of_constraints= 0

        self.directions = [self.MAXIMIZE]
        self.labels = ['Maskcat']


    def create_solution(self) -> MaskcatSolution:
        """ Creates a random_search solution to the problem.

        :return: Solution. """
        new_solution = MaskcatSolution(self.number_of_variables, self.number_of_objectives)

        new_solution.variables[0] = [mask for mask in range (self.number_of_variables)]

        return new_solution

    def evaluate(self, solution: MaskcatSolution) -> MaskcatSolution:
        """ Evaluate a solution. For any new problem inheriting from :class:`Problem`, this method should be
        replaced. Note that this framework ASSUMES minimization, thus solutions must be evaluated in consequence.

        :return: Evaluated solution. """

        for mask in solution.variables:
            puntuation = execHashcat(mask)
            x = self.masksResults.get("punctuations")
            x.append(puntuation)
            x.sort()
            pos = x.index(puntuation)
            y = self.masksResults.get("masksList") 
            y.insert(pos, mask)
            self.masksResults["masksList"] = y
            self.masksResults["punctuations"]= x
        
        masksBestPunctuation = self.masksResults.get('punctuations')
        masksBestPunctuation = masksBestPunctuation.pop()

        solution.objectives[0] =-1.0 * masksBestPunctuation
        return solution

    def get_name(self) -> str:
        return 'Maskcat'



