from typing import TypeVar, List

from jmetal.config import store
from jmetal.core.operator import Mutation, Crossover, Selection
from jmetal.core.problem import Problem
from jmetal.util.evaluator import Evaluator
from jmetal.util.generator import Generator
from jmetal.util.termination_criterion import TerminationCriterion

from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm

S = TypeVar('S')
R = TypeVar('R')

class GeneticAlgorithm_Reset (GeneticAlgorithm):
    def __init__(self,
                 problem: Problem,
                 population_size: int,
                 offspring_population_size: int,
                 generation_reset_number:int,
                 mutation: Mutation,
                 crossover: Crossover,
                 selection: Selection,
                 termination_criterion: TerminationCriterion = store.default_termination_criteria,
                 population_generator: Generator = store.default_generator,
                 population_evaluator: Evaluator = store.default_evaluator):
        super(GeneticAlgorithm_Reset, self).__init__(
            problem=problem,
            population_size=population_size,
            offspring_population_size=offspring_population_size,
            mutation= mutation,
            crossover= crossover,
            selection= selection,
            termination_criterion= termination_criterion,
            population_generator= population_generator,
            population_evaluator= population_evaluator)

        self.generation_counter = 0
        self.generation_reset_number = generation_reset_number
    
    def reproduction(self, mating_population: List[S]) -> List[S]:
        self.generation_counter +=1

        number_of_parents_to_combine = self.crossover_operator.get_number_of_parents()

        if len(mating_population) % number_of_parents_to_combine != 0:
            raise Exception('Wrong number of parents')

        offspring_population = []

        if self.generation_counter % self.generation_reset_number != 0:
            for i in range(0, self.offspring_population_size, number_of_parents_to_combine):
                parents = []
                for j in range(number_of_parents_to_combine):
                    parents.append(mating_population[i + j])

                offspring = self.crossover_operator.execute(parents)

                for solution in offspring:
                    self.mutation_operator.execute(solution)
                    offspring_population.append(solution)
                    if len(offspring_population) >= self.offspring_population_size:
                        break
        else:
            self.solutions.sort(key=lambda s: s.objectives[0])
            offspring_population = self.create_initial_solutions()
            offspring_population = offspring_population[:-1]
            offspring_population.append(self.solutions[0])

        return offspring_population