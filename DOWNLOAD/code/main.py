import datetime
from maskcat import Maskcat

import maskcat_config

def update_config(population:int, generations:int):
    maskcat_config.POPULATION_SIZE = population
    maskcat_config.OFFSPRING_POPULATION = population
    maskcat_config.MAX_EVALUATIONS = population * generations
    maskcat_config.DIRECTORY_OUTPUT_FILES= "./experiments/maskcat_loop{}-{}_generational".format(population, generations)

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


update_config(300, 100)
inicio = datetime.datetime.now()
Maskcat().run()
fin = datetime.datetime.now()
update_times(inicio, fin)

#update_config(200, 100)
#inicio = datetime.datetime.now()
#Maskcat().run()
#fin = datetime.datetime.now()
#update_times(inicio, fin)

update_config(50, 200)
inicio = datetime.datetime.now()
Maskcat().run()
fin = datetime.datetime.now()
update_times(inicio, fin)

#update_config(100, 200)
#inicio = datetime.datetime.now()
#Maskcat().run()
#fin = datetime.datetime.now()
#update_times(inicio, fin)

#update_config(200, 200)
#inicio = datetime.datetime.now()
#Maskcat().run()
#fin = datetime.datetime.now()
#update_times(inicio, fin)

#update_config(300, 200)
#inicio = datetime.datetime.now()
#Maskcat().run()
#fin = datetime.datetime.now()
#update_times(inicio, fin)
