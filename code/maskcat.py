import json
from jmetal_maskcat import MaskcatProblem, MaskcatSolution

from jmetal.algorithm.singleobjective import GeneticAlgorithm

from jmetal.util.termination_criterion import StoppingByEvaluations
import jmetal
from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, print_variables_to_file
import jmetal.util.observer as observers

from maskcat_operators import MaskcatSPXCrossover, MaskcatUniformMutation
from maskcat_observers import MaskcatObserver


historico = {}
scores = []
max_evaluations = 600

def mean(list):
    sum = 0
    for element in list:
        sum = sum + element
    
    return sum/len(list)

def maskcat_single(tag:str):
    problem = MaskcatProblem()

    algorithm = GeneticAlgorithm(problem=problem,
                                population_size=10, 
                                offspring_population_size=10, 
                                mutation=MaskcatUniformMutation(0.1) , 
                                selection= jmetal.operator.selection.BinaryTournamentSelection(), 
                                crossover=MaskcatSPXCrossover(0.7),
                                termination_criterion=StoppingByEvaluations(max_evaluations))

    basic = observers.BasicObserver(frequency=1.0)
    algorithm.observable.register(observer=basic)

    progress_bar = observers.ProgressBarObserver(max=max_evaluations)
    algorithm.observable.register(progress_bar)

    maskcat_observer = MaskcatObserver("../maskcat_generaciones", "maskcat_generaciones_{}.csv".format(tag), 1.0)
    algorithm.observable.register(maskcat_observer)

    algorithm.run()

    solutions = algorithm.get_result()
    print(str(solutions))

    masksHistory = problem.get_masksHistory()
    fd1 = open("../results/maskcatHistory_{}.csv".format(tag), "w")
    masksHistoryCSV = []
    for line in masksHistory:
        masksHistoryCSV.append(str(line[0])+","+str(line[1])+"\n")    
    fd1.writelines(masksHistoryCSV)
    fd1.close()

    masksResults = problem.get_maskResults()
    masksResults["Solution"] = str(solutions)

    fd2 = open("../results/maskcatResults_{}.json".format(tag), "w")
    json.dump(masksResults, fd2)
    fd2.close()


def maskcat_loop():
    for i in range (0, 30):
        problem = MaskcatProblem()

        algorithm = GeneticAlgorithm(problem=problem,
                                    population_size=10, 
                                    offspring_population_size=10, 
                                    mutation=MaskcatUniformMutation(0.1) , 
                                    selection= jmetal.operator.selection.BinaryTournamentSelection(), 
                                    crossover=MaskcatSPXCrossover(0.7),
                                    termination_criterion=StoppingByEvaluations(max_evaluations))

        basic = observers.BasicObserver(frequency=1.0)
        algorithm.observable.register(observer=basic)

        progress_bar = observers.ProgressBarObserver(max=max_evaluations)
        algorithm.observable.register(progress_bar)

        maskcat_observer = MaskcatObserver("../maskcat_generaciones", "maskcat_generaciones_rep{}.csv".format(i), 1.0)
        algorithm.observable.register(maskcat_observer)

        algorithm.run()

        solutions = algorithm.get_result()
        print(str(solutions))

        masksHistory = problem.get_masksHistory()
        fd1 = open("../results/maskcatHistory_rep{}.csv".format(i), "w")
        masksHistoryCSV = []
        for line in masksHistory:
            masksHistoryCSV.append(str(line[0])+","+str(line[1])+"\n")    
        fd1.writelines(masksHistoryCSV)
        fd1.close()

        masksResults = problem.get_maskResults()
        masksResults["Solution"] = str(solutions)

        fd2 = open("../results/maskcatResults_rep{}.json".format(i), "w")
        json.dump(masksResults, fd2)
        fd2.close()

        historico[i] = {"Array mascara":solutions.getMask(), "Puntuacion":solutions.getScore()}
        scores.append(solutions.getScore())

    fd3 = open("../results/estadisticas_historico.json", "w")
    json.dump(historico, fd3)
    fd3.close()

# scores.sort()

# max = scores[0]
# min = scores(len(scores)-1)

# scores_mean = mean(scores)




print('TERMINADO\n')