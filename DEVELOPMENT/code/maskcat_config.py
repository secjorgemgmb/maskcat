import datetime


#========== Directories to open or write files ==========
OUTPUT_FILES = True
DIRECTORY_OUTPUT_FILES = "../experiments/maskcat_generational_{}".format(datetime.date.today())
WORDLIST_ROUTE = "../wordlists/shuffled_top_1M_MD5.txt"

#========== Maskcat problem execution variables ==========
MASK_LEN=7
PREDEFINED_MASKS=0

#========== Maskcat GeneticAlgorithm execution variables ==========
GENERATIONAL = False
POPULATION_RESET = False
POPULATION_RESET_NUMBER = 1
POPULATION_SIZE=100
OFFSPRING_POPULATION = 100
MAX_EVALUATIONS=10000
REPETITIONS=1
