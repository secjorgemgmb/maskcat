import datetime
from maskcat import Maskcat
import sys


import maskcat_config

def update_config(population:int, generations:int, probability:int):
    maskcat_config.POPULATION_SIZE = population
    maskcat_config.OFFSPRING_POPULATION = population
    maskcat_config.MAX_EVALUATIONS = population * generations
    maskcat_config.MUTATION_PROB = float(probability/100)
    maskcat_config.DIRECTORY_OUTPUT_FILES= "/home/jmcolmenar/maskcat/MASKCAT/experiments/maskcat_loop{}-{}_{}".format(population, generations, probability)

def update_times(t_inicio, t_fin):
    if maskcat_config.OUTPUT_FILES:
        fd = open ("{}/times/times.txt".format(maskcat_config.DIRECTORY_OUTPUT_FILES), "w")
        fd.write('''Experimento : maskcat (generational = {})
        Poblacion = {}
        Num generaciones = {}
        Num iteraciones = {}
        Inicio: {}
        Fin: {}\n'''.format(maskcat_config.GENERATIONAL, maskcat_config.POPULATION_SIZE,(maskcat_config.MAX_EVALUATIONS / maskcat_config.POPULATION_SIZE), maskcat_config.REPETITIONS ,t_inicio, t_fin))
        fd.close()

    print("Hora de inicio= {}\nHora de fin= {}\n".format(t_inicio, t_fin))

params = sys.argv[1:]
update_config(int(params[0]), int(params[1]), int(params[2]))
inicio = datetime.datetime.now()
Maskcat().run()
fin = datetime.datetime.now()
update_times(inicio, fin)
