import datetime
from maskcat import Maskcat

import maskcat_config


inicio = datetime.datetime.now()
Maskcat().run()
fin = datetime.datetime.now()

if maskcat_config.OUTPUT_FILES:
    fd = open ("{}/times/times.txt".format(maskcat_config.DIRECTORY_OUTPUT_FILES), "w")
    fd.write('''Experimento : maskcat normal poblacion tamaño 100 y 100 generaciones
    Inicio: {}
    Fin: {}'''.format(inicio, fin))
    fd.close()
else:
    print("Hora de inicio= {}\nHora de fin= {}\n".format(inicio, fin))
