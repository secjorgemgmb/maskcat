from ctypes.wintypes import WORD
import datetime


GENERATIONAL = True
POPULATION_SIZE=300
OFFSPRING_POPULATION =300
MAX_EVALUATIONS=30000
REPETITIONS=10

DIRECTORY_OUTPUT_FILES = "./experiments/maskcat_loop300-100_prob10"

MUTATION_PROB = 0.1
CROSSOVER_PROB = 0.7

#========== Directories to open or write files ==========
# Generar ficheros para analizar la ejecución
OUTPUT_FILES = True
#DIRECTORY_OUTPUT_FILES = "./experiments/maskcat_prueba_{}".format(datetime.date.today())


#Preferible ruta absoluta del fichero wordlist
# WORDLIST_ROUTE = "C:\\Users\\Jorge\\Desktop\\TFG\\maskcat\\DOWNLOAD\\wordlists\\rockyouMD5_1.txt"

WORDLIST_ROUTE = "/home/jmcolmenar/maskcat/MASKCAT/wordlists/experiments-file_MD5.txt"


#========== Maskcat Command ==========
# Modificar los valores a corde al comando que se quiera ejecutar, no introducir máscara (se hace en hashcat_exec.py), ruta de wordlist se sextrae de
# la variable definida con anterioridad
#HASHCAT_COMMAND = "hashcat.cmd -m 0 -a 3 -d 1 --runtime=600 --status-json -O --potfile-disable --logfile-disable {}".format(WORDLIST_ROUTE)

HASHCAT_COMMAND = "NONE"

#========== Maskcat problem execution variables ==========
#MASK_LEN = Longitud de la máscara - 1
MASK_LEN=7
PREDEFINED_MASKS=0

