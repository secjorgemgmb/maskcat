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

class GeneticAlgorithm_Generational (GeneticAlgorithm):
    def __init__(self,
                 problem: Problem,
                 population_size: int,
                 offspring_population_size: int,
                 mutation: Mutation,
                 crossover: Crossover,
                 selection: Selection,
                 termination_criterion: TerminationCriterion = store.default_termination_criteria,
                 population_generator: Generator = store.default_generator,
                 population_evaluator: Evaluator = store.default_evaluator):
        super(GeneticAlgorithm_Generational, self).__init__(
            problem=problem,
            population_size=population_size,
            offspring_population_size=offspring_population_size,
            mutation= mutation,
            crossover= crossover,
            selection= selection,
            termination_criterion= termination_criterion,
            population_generator= population_generator,
            population_evaluator= population_evaluator)
    
    def replacement(self, population: List[S], offspring_population: List[S]) -> List[S]:
        population.sort(key=lambda s: s.objectives[0])
        offspring_population.sort(key=lambda s: s.objectives[0])

        if population[0].objectives[0] < offspring_population[0].objectives[0]:
            offspring_population = offspring_population[:-1]
            offspring_population.append(population[0])
            offspring_population.sort(key=lambda s: s.objectives[0])

        return offspring_population