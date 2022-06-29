import datetime
from maskcat import Maskcat
import sys

import maskcat_config

def update_config(population:int, generations:int):
    maskcat_config.POPULATION_SIZE = population
    maskcat_config.GENERATION_NUMBER = generations
    maskcat_config.DIRECTORY_OUTPUT_FILES= "./experiments/prueba_poblacion{}-generaciones{}".format(population, generations)

def update_times(t_inicio, t_fin):
    if maskcat_config.OUTPUT_FILES:
        fd = open ("{}/times/times.txt".format(maskcat_config.DIRECTORY_OUTPUT_FILES), "w")
        fd.write('''Experimento : maskcat (generational = {})
        Poblacion = {}
        Num generaciones = {}
        Num iteraciones = {}
        Inicio: {}
        Fin: {}\n'''.format(maskcat_config.GENERATIONAL, maskcat_config.POPULATION_SIZE,maskcat_config.GENERATION_NUMBER, maskcat_config.REPETITIONS ,t_inicio, t_fin))
        fd.close()

    print("Hora de inicio= {}\nHora de fin= {}\n".format(t_inicio, t_fin))

params = sys.argv[1:]

if len(params) == 0:
    inicio = datetime.datetime.now()
    Maskcat().run()
    fin = datetime.datetime.now()
    update_times(inicio, fin)
elif len(params) ==2:
    update_config(int(params[0]), int(params[1]))
    inicio = datetime.datetime.now()
    Maskcat().run()
    fin = datetime.datetime.now()
    update_times(inicio, fin)
else:
    print("Número de parámetros no válido, revisa la información de uso")

