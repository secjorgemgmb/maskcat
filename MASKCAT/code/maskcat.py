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

import maskcat_config
from maskcat_genetics import GeneticAlgorithm_Reset, GeneticAlgorithm_Generational


LOGGER = logging.getLogger('jmetal')

class Maskcat ():
    def __init__(self) -> None:
        self.historico = {}
        self.scores = []
        self.cache = {}
        self.output_files = maskcat_config.OUTPUT_FILES
        self.generational = maskcat_config.GENERATIONAL

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

    def run(self):
        tag = ""
        if self.output_files:
            directories = self.create_folders(maskcat_config.DIRECTORY_OUTPUT_FILES)

        data_frame_iteraciones = pd.DataFrame(columns=["Iteracion", "Puntuacion", "Array"])
        for i in range (0, maskcat_config.REPETITIONS):
            if maskcat_config.REPETITIONS > 1:
                tag = "_rep{}".format(i)

            problem = MaskcatProblem(self.cache)

            if self.generational:
                algorithm = GeneticAlgorithm_Generational(problem=problem,
                                            population_size=maskcat_config.POPULATION_SIZE, 
                                            offspring_population_size=maskcat_config.OFFSPRING_POPULATION,
                                            mutation=MaskcatUniformMutation(maskcat_config.MUTATION_PROB) , 
                                            selection= jmetal.operator.selection.BinaryTournamentSelection(), 
                                            crossover=MaskcatSPXCrossover(maskcat_config.CROSSOVER_PROB),
                                            termination_criterion=StoppingByEvaluations(maskcat_config.MAX_EVALUATIONS))
            else:
                algorithm = GeneticAlgorithm(problem=problem,
                                            population_size=maskcat_config.POPULATION_SIZE, 
                                            offspring_population_size=maskcat_config.OFFSPRING_POPULATION,
                                            mutation=MaskcatUniformMutation(maskcat_config.MUTATION_PROB) , 
                                            selection= jmetal.operator.selection.BinaryTournamentSelection(), 
                                            crossover=MaskcatSPXCrossover(maskcat_config.CROSSOVER_PROB),
                                            termination_criterion=StoppingByEvaluations(maskcat_config.MAX_EVALUATIONS))

            basic = observers.BasicObserver(frequency=1.0)
            algorithm.observable.register(observer=basic)

            progress_bar = observers.ProgressBarObserver(max=maskcat_config.MAX_EVALUATIONS)
            algorithm.observable.register(progress_bar)

            if self.output_files:
                maskcat_observer = MaskcatObserver(directories[1], "maskcat_generaciones{}.csv".format(tag), 1.0)
                algorithm.observable.register(maskcat_observer)

            algorithm.run()

            solutions = algorithm.get_result()
            print(str(solutions))

            if self.output_files:
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

        if self.output_files:
            file_2 = open("{}/experiment_cache.json".format(directories[0], tag), "w")
            json.dump(self.cache, file_2)
            file_2.close()

        if maskcat_config.REPETITIONS > 1 and self.output_files:

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
