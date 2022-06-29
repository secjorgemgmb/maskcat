from functools import total_ordering
from maskcat_problem import MaskcatProblem, MaskcatSolution
import jmetal.core.operator as operators

import copy
import random
from typing import List
from jmetal.util.ckecking import Check


class MaskcatSPXCrossover(operators.Crossover[MaskcatSolution, MaskcatSolution]):
    '''One-poit crossover'''

    def __init__(self, probability: float):
        super(MaskcatSPXCrossover, self).__init__(probability=probability)

    def execute(self, parents: List[MaskcatSolution]) -> List[MaskcatSolution]:
        Check.that(type(parents[0]) is MaskcatSolution, "Solution type invalid")
        Check.that(type(parents[1]) is MaskcatSolution, "Solution type invalid")
        Check.that(len(parents) == 2, 'The number of parents is not two: {}'.format(len(parents)))

        offspring = [copy.deepcopy(parents[0]), copy.deepcopy(parents[1])]
        rand = random.random()

        if rand <= self.probability:
            len_of_masks = parents[0].get_number_of_masks()

            crossover_point = random.randint(1, len_of_masks)

            mask_copy_1 = copy.copy(parents[0].variables)
            mask_copy_2 = copy.copy(parents[1].variables)

            for i in range(0, crossover_point):
                swap = mask_copy_1[i]
                mask_copy_1[i] = mask_copy_2[i]
                mask_copy_2[i] = swap


            offspring[0].variables = mask_copy_1
            offspring[1].variables = mask_copy_2

        return offspring
        
    def get_number_of_parents(self) -> int:
        return 2

    def get_number_of_children(self) -> int:
        return 2

    def get_name(self) -> str:
        return 'Maskcat single point crossover'

class MaskcatUniformMutation(operators.Mutation[MaskcatSolution]):

    def __init__(self, probability: float, perturbation: float = 0.5):
        super(MaskcatUniformMutation, self).__init__(probability=probability)
        self.perturbation = perturbation

    def execute(self, solution: MaskcatSolution) -> MaskcatSolution:
        Check.that(type(solution) is MaskcatSolution, "Solution type invalid")
        rand = random.random()

        if rand <= self.probability:
            gen = random.randint(0, len(solution.variables)-1)

            tmp = (random.randint(0, 4))
            while tmp == solution.variables[gen]:
                tmp = (random.randint(0, 4))
            solution.variables[gen] = tmp

        return solution

    def get_name(self):
        return 'Maskcat uniform mutation'