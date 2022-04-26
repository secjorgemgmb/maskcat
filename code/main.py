import datetime
from maskcat import Maskcat

import maskcat_config


inicio = datetime.datetime.now()
Maskcat().run()
fin = datetime.datetime.now()

fd = open ("{}/times/times.txt".format(maskcat_config.DIRECTORY), "w")
fd.write('''Experimento : maskcat normal poblacion tamaño 100 y 100 generaciones
Inicio: {}
Fin: {}'''.format(inicio, fin))
fd.close()
