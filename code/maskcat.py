import json
import logging
from pathlib import Path
import copy

from maskcat_problem import MaskcatProblem

from jmetal.algorithm.singleobjective import GeneticAlgorithm

from jmetal.util.termination_criterion import StoppingByEvaluations
import jmetal
from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, print_variables_to_file
import jmetal.util.observer as observers

from maskcat_operators import MaskcatSPXCrossover, MaskcatUniformMutation
from maskcat_observers import MaskcatObserver

import pandas as pd

from maskcat_genetics import GeneticAlgorithm_Reset


LOGGER = logging.getLogger('jmetal')

class Maskcat ():
    def __init__(self, reset:bool = False) -> None:
        self.historico = {}
        self.scores = []
        self.cache = {}
        self.reset = reset

    def create_folders (self, directory:str):
        if not Path(directory).is_dir():
            LOGGER.warning('Directory {} does not exist. Creating it.'.format(directory))
            Path(directory).mkdir(parents=True)
        results_directory = directory + "/results"
        generations_directory = directory + "/generations"
        times_directory = directory + "/times"
        if not Path(results_directory).is_dir():
            LOGGER.warning('Directory {} does not exist. Creating it.'.format(results_directory))
            Path(results_directory).mkdir(parents=True)
        if not Path(generations_directory).is_dir():
            LOGGER.warning('Directory {} does not exist. Creating it.'.format(generations_directory))
            Path(generations_directory).mkdir(parents=True)
        if not Path(times_directory).is_dir():
            LOGGER.warning('Directory {} does not exist. Creating it.'.format(times_directory))
            Path(times_directory).mkdir(parents=True)
        return [results_directory, generations_directory]

    def run(self, OS:str, main_directory:str, wordlist_route:str, repetitions:int, population_size:int, offspring_population_size:int, max_evaluations:int, mask_len:int, predefined_masks:int, generations_reset_number:int=0):
        tag = ""
        directories = self.create_folders(main_directory)

        data_frame_iteraciones = pd.DataFrame(columns=["Iteracion", "Puntuacion", "Array"])
        for i in range (0, repetitions):
            if repetitions > 1:
                tag = "_rep{}".format(i)

            problem = MaskcatProblem(self.cache, wordlist_route, OS=OS, pass_len=mask_len, predefined_masks=predefined_masks, generation_size=population_size)

            if self.reset:
                if generations_reset_number > 0:
                    algorithm = GeneticAlgorithm_Reset(problem=problem,
                                            population_size=population_size, 
                                            offspring_population_size=offspring_population_size,
                                            generation_reset_number= generations_reset_number, 
                                            mutation=MaskcatUniformMutation(0.1) , 
                                            selection= jmetal.operator.selection.BinaryTournamentSelection(), 
                                            crossover=MaskcatSPXCrossover(0.7),
                                            termination_criterion=StoppingByEvaluations(max_evaluations))
                else:
                    raise ValueError("Number of generations to reset population not valid it has to be over 0")
            else:
                algorithm = GeneticAlgorithm(problem=problem,
                                            population_size=population_size, 
                                            offspring_population_size=offspring_population_size,
                                            mutation=MaskcatUniformMutation(0.1) , 
                                            selection= jmetal.operator.selection.BinaryTournamentSelection(), 
                                            crossover=MaskcatSPXCrossover(0.7),
                                            termination_criterion=StoppingByEvaluations(max_evaluations))

            basic = observers.BasicObserver(frequency=1.0)
            algorithm.observable.register(observer=basic)

            progress_bar = observers.ProgressBarObserver(max=max_evaluations)
            algorithm.observable.register(progress_bar)


            maskcat_observer = MaskcatObserver(directories[1], "maskcat_generaciones{}.csv".format(tag), 1.0)
            algorithm.observable.register(maskcat_observer)

            algorithm.run()

            solutions = algorithm.get_result()
            print(str(solutions))

            masks_history = problem.get_masks_history()
            file_1 = open("{}/maskcatHistory{}.csv".format(directories[0], tag), "w")
            masks_historyCSV = []
            masks_historyCSV.append("Array;Mask;Score;Generacion\n")
            for line in masks_history:
                masks_historyCSV.append("{};{};{};{}\n".format(line[0], line[1], line[2], line[3]))    
            file_1.writelines(masks_historyCSV)
            file_1.close()

            data_frame_iteraciones = data_frame_iteraciones.append({"Iteracion":i, "Puntuacion":solutions.get_score(), "Array":solutions.get_mask()}, ignore_index=True)
            self.scores.append(solutions.get_score())

        file_2 = open("{}/maskcatResults{}.json".format(directories[0], tag), "w")
        json.dump(self.cache, file_2)
        file_2.close()

        if repetitions > 1:

            data_frame_iteraciones.to_csv("{}/estadisticas_historico.csv".format(directories[0]), index=False, sep=";")

            media = data_frame_iteraciones["Puntuacion"].mean()
            max = data_frame_iteraciones["Puntuacion"].max()
            min = data_frame_iteraciones["Puntuacion"].min()
            desv_est = data_frame_iteraciones["Puntuacion"].std()
            moda = data_frame_iteraciones["Puntuacion"].mode()[0]
            mediana = data_frame_iteraciones["Puntuacion"].median()

            file_3 = open("{}/estadisticas.txt".format(directories[0]), "w")
            file_3.write('''Media = {}\nMax = {}\nMin = {}\nDesviacion estandar = {}\nModa = {}\nMediana = {}'''.format(media, min, max, desv_est, moda, mediana))
            file_3.close()
