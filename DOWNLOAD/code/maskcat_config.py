import datetime


#========== Directories to open or write files ==========
OUTPUT_FILES = False
DIRECTORY_OUTPUT_FILES = ".\experiments\maskcat_no-output_{}".format(datetime.date.today())
WORDLIST_ROUTE = "C:\\Users\\Jorge\\Desktop\\TFG\\maskcat\\DOWNLOAD\\wordlists\\shuffled_top_1M_MD5.txt"

#========== Maskcat problem execution variables ==========
MASK_LEN=7
PREDEFINED_MASKS=0

#========== Maskcat GeneticAlgorithm execution variables ==========
GENERATIONAL = False

POPULATION_RESET = False
POPULATION_RESET_NUMBER = 1

POPULATION_SIZE=50
OFFSPRING_POPULATION = 50
MAX_EVALUATIONS=5000
REPETITIONS=1
