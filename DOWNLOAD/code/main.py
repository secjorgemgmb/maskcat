import datetime
from maskcat import Maskcat

import maskcat_config


inicio = datetime.datetime.now()
Maskcat().run()
fin = datetime.datetime.now()

if maskcat_config.OUTPUT_FILES:
    fd = open ("{}/times/times.txt".format(maskcat_config.DIRECTORY_OUTPUT_FILES), "w")
    fd.write('''Experimento : prueba rendimiento maskcat poblacion 500, 100 generacines algortimo generacional
    Inicio: {}
    Fin: {}\n'''.format(inicio, fin))
    fd.close()

print("Hora de inicio= {}\nHora de fin= {}\n".format(inicio, fin))
