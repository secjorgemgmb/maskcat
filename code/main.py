import datetime
from maskcat import maskcat_execution

date = datetime.date.today()

directory_generations = "../maskcat_generaciones/{}".format(date)
directory_results = "../results/{}".format(date)
tag = "maskcat_pruebaCacheGlobal_{}".format(date)
wordlist_route = "../wordlists/shuffled_top_1M_MD5.txt"
repetitions=1
population_size=50
offspring_population_size = 50
max_evaluations=5000
mask_len=7
predefined_masks=0

inicio = datetime.datetime.now()
maskcat_execution(directory_generations=directory_generations,
    directory_results=directory_results,
    tag=tag, wordlist_route=wordlist_route,
    repetitions=repetitions,
    population_size=population_size,
    offspring_population_size=offspring_population_size,
    max_evaluations=max_evaluations,
    mask_len=mask_len,
    predefined_masks=predefined_masks)
fin = datetime.datetime.now()

fd = open ("../tiempos/times_{}.txt".format(tag), "w")
fd.write('''Experimento : prueba chache global 
Inicio: {}
Fin: {}'''.format(inicio, fin))
fd.close()