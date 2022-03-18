import json
from maskcat_problem import MaskcatProblem, MaskcatSolution

from jmetal.algorithm.singleobjective import GeneticAlgorithm

from jmetal.util.termination_criterion import StoppingByEvaluations
import jmetal
from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, print_variables_to_file
import jmetal.util.observer as observers

from maskcat_operators import MaskcatSPXCrossover, MaskcatUniformMutation
from maskcat_observers import MaskcatObserver

import pandas as pd


historico = {}
scores = []
max_evaluations = 600

def mean(list):
    sum = 0
    for element in list:
        sum = sum + element
    
    return sum/len(list)

def maskcat_single(tag:str, wordlist_route:str):
    problem = MaskcatProblem(wordlist_route, pass_len=7, predefined_masks=2)

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


def maskcat_loop(tag:str, wordlist_route:str):
    df = pd.DataFrame(columns=["Iteracion", "Puntuacion", "Array"])
    for i in range (0, 30):
        problem = MaskcatProblem(wordlist_route, pass_len=7, predefined_masks=2)

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

        maskcat_observer = MaskcatObserver("../maskcat_generaciones", "maskcat_generaciones_{}_rep{}.csv".format(tag, i), 1.0)
        algorithm.observable.register(maskcat_observer)

        algorithm.run()

        solutions = algorithm.get_result()
        print(str(solutions))

        masksHistory = problem.get_masksHistory()
        fd1 = open("../results/maskcatHistory_{}_rep{}.csv".format(tag, i), "w")
        masksHistoryCSV = []
        for line in masksHistory:
            masksHistoryCSV.append(str(line[0])+","+str(line[1])+"\n")    
        fd1.writelines(masksHistoryCSV)
        fd1.close()

        masksResults = problem.get_maskResults()
        masksResults["Solution"] = str(solutions)

        fd2 = open("../results/maskcatResults_{}_rep{}.json".format(tag, i), "w")
        json.dump(masksResults, fd2)
        fd2.close()

        df = df.append({"Iteracion":i, "Puntuacion":solutions.getScore(), "Array":solutions.getMask()}, ignore_index=True)
        scores.append(solutions.getScore())
    # df.to_json(df,"../results/estadisticas_historico_{}.json".format(tag))
    df.to_csv("../results/estadisticas_historico_{}.json".format(tag), index=False)

    media = df["Puntuacion"].mean()
    max = df["Puntuacion"].max()
    min = df["Puntuacion"].min()
    desv_est = df["Puntuacion"].std()
    moda = df["Puntuacion"].mode()[0]
    mediana = df["Puntuacion"].median()

    fd3 = open("../results/estadisticas_{}.txt".format(tag), "w")
    fd3.write('''Media = {}\n
    Max = {}\n
    Min = {}\n
    Desviacion estandar = {}\n
    Moda = {}\n
    Mediana = {}'''.format(media, max, min, desv_est, moda, mediana))
    fd3.close()

    
    

def maskcat_single_longpass(tag:str, wordlist_route:str):
    problem = MaskcatProblem(wordlist_route, pass_len=12, predefined_masks=2)

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

    maskcat_observer = MaskcatObserver("../maskcat_generaciones", "maskcat_generaciones_longPass_{}.csv".format(tag), 1.0)
    algorithm.observable.register(maskcat_observer)

    algorithm.run()

    solutions = algorithm.get_result()
    print(str(solutions))

    masksHistory = problem.get_masksHistory()
    fd1 = open("../results/maskcatHistory_longPass_{}.csv".format(tag), "w")
    masksHistoryCSV = []
    for line in masksHistory:
        masksHistoryCSV.append(str(line[0])+","+str(line[1])+"\n")    
    fd1.writelines(masksHistoryCSV)
    fd1.close()

    masksResults = problem.get_maskResults()
    masksResults["Solution"] = str(solutions)

    fd2 = open("../results/maskcatResults_longPass_{}.json".format(tag), "w")
    json.dump(masksResults, fd2)
    fd2.close()
