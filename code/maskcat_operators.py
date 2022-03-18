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

            # 1. Get the total number of masks in solution 1
            total_number_of_masks = parents[0].get_number_of_masks()
            total_number_of_masks2 = parents[1].get_number_of_masks()
            # 2. Calculate the point to make crossover
            crossover_point = random.randint(0, total_number_of_masks)

            # 3. Check number of masks in solution 2 >= crossover_point
            if total_number_of_masks2 < crossover_point:
                crossover_point = random.randint(0, total_number_of_masks2)

            # 4. Recombine solutions chromosomes based on crossover_point
            maskCopy1 = copy.copy(parents[0].variables)
            maskCopy2 = copy.copy(parents[1].variables)

            for i in range(0, crossover_point):
                swap = maskCopy1[i]
                maskCopy1[i] = maskCopy2[i]
                maskCopy2[i] = swap


            offspring[0].variables = maskCopy1
            offspring[1].variables = maskCopy2

            # # 1. Get the total number of bits
            # total_number_of_masks = parents[0].get_number_of_masks()

            # # 2. Calculate the point to make the crossover
            # crossover_point = random.randrange(0, total_number_of_masks)

            # # 3. Compute the variable containing the crossover bit
            # variable_to_cut = 0
            # bits_count = len(parents[1].variables[variable_to_cut])
            # while bits_count < (crossover_point + 1):
            #     variable_to_cut += 1
            #     bits_count += len(parents[1].variables[variable_to_cut])

            # # 4. Compute the bit into the selected variable
            # diff = bits_count - crossover_point
            # crossover_point_in_variable = len(parents[1].variables[variable_to_cut]) - diff

            # # 5. Apply the crossover to the variable
            # bitset1 = copy.copy(parents[0].variables[variable_to_cut])
            # bitset2 = copy.copy(parents[1].variables[variable_to_cut])

            # for i in range(crossover_point_in_variable, len(bitset1)):
            #     swap = bitset1[i]
            #     bitset1[i] = bitset2[i]
            #     bitset2[i] = swap

            # offspring[0].variables[variable_to_cut] = bitset1
            # offspring[1].variables[variable_to_cut] = bitset2

            # # 6. Apply the crossover to the other variables
            # for i in range(variable_to_cut + 1, parents[0].number_of_variables):
            #     offspring[0].variables[i] = copy.deepcopy(parents[1].variables[i])
            #     offspring[1].variables[i] = copy.deepcopy(parents[0].variables[i])

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

        for i in range(solution.number_of_variables):
            rand = random.random()

            if rand <= self.probability:
                tmp = (random.randint(0, 4))
                
                solution.variables[i] = tmp

        return solution

    def get_name(self):
        return 'Maskcat uniform mutation'