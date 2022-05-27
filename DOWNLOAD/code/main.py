import datetime
from maskcat import Maskcat

import maskcat_config


inicio = datetime.datetime.now()
Maskcat().run()
fin = datetime.datetime.now()

if maskcat_config.OUTPUT_FILES:
    fd = open ("{}/times/times.txt".format(maskcat_config.DIRECTORY_OUTPUT_FILES), "w")
    fd.write('''Experimento : maskcat (generational = {})
    Poblacion = {}
    Num generaciones = {}
    Num iteraciones = {}
    Inicio: {}
    Fin: {}\n'''.format(maskcat_config.GENERATIONAL, maskcat_config.POPULATION_SIZE,(maskcat_config.MAX_EVALUATIONS / maskcat_config.POPULATION_SIZE), maskcat_config.REPETITIONS ,inicio, fin))
    fd.close()

print("Hora de inicio= {}\nHora de fin= {}\n".format(inicio, fin))
