import datetime
from turtle import update
from maskcat import Maskcat

import maskcat_config

def update_config(population:int, generations:int):
    maskcat_config.POPULATION_SIZE = population
    maskcat_config.OFFSPRING_POPULATION = population
    maskcat_config.DIRECTORY_OUTPUT_FILES= "./experiments/prueba{}-{}".format(population, generations)
    maskcat_config.MAX_EVALUATIONS = population * generations


def update_times(t_inicio, t_fin):
    if maskcat_config.OUTPUT_FILES:
        fd = open ("{}/times/times.txt".format(maskcat_config.DIRECTORY_OUTPUT_FILES), "w")
        fd.write('''Experimento : prueba rendimiento maskcat poblacion 50, 100 generacines algortimo generacional, bucle 10 iteraciones
        Inicio: {}
        Fin: {}\n'''.format(t_inicio, t_fin))
        fd.close()

    print("Hora de inicio= {}\nHora de fin= {}\n".format(t_inicio, t_fin))


inicio = datetime.datetime.now()
Maskcat().run()
fin = datetime.datetime.now()
update_times(inicio, fin)

update_config(20, 1)
inicio = datetime.datetime.now()
Maskcat().run()
fin = datetime.datetime.now()
update_times(inicio, fin)
