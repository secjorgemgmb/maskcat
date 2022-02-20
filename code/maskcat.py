from audioop import cross
from jmetal_maskcat import MaskcatProblem, MaskcatSolution

from jmetal.algorithm.singleobjective import GeneticAlgorithm

from jmetal.util.termination_criterion import StoppingByEvaluations
import jmetal
from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, print_variables_to_file

from maskcat_operators import MaskcatSPXCrossover, MaskcatUniformMutation

problem = MaskcatProblem()

algorithm = GeneticAlgorithm(problem=problem,
                            population_size=10, 
                            offspring_population_size=10, 
                            mutation=MaskcatUniformMutation(0.1) , 
                            selection= jmetal.operator.selection.BinaryTournamentSelection(), 
                            crossover=MaskcatSPXCrossover(0.7),
                            termination_criterion=StoppingByEvaluations(600))

algorithm.run()

front = algorithm.get_result()

# save to files
# print_function_values_to_file(front, '/Users/jorgemartinezgarcia/OneDrive - Universidad Rey Juan Carlos/TFG/maskcat/functio_values_to_file')
# print_variables_to_file(front, '/Users/jorgemartinezgarcia/OneDrive - Universidad Rey Juan Carlos/TFG/maskcat/variables_to_file')

print('TERMINADO\n'+str(front))