from ctypes.wintypes import WORD
import datetime


#========== Directories to open or write files ==========
# Generar ficheros para analizar la ejecución
OUTPUT_FILES = True
#DIRECTORY_OUTPUT_FILES = "./experiments/maskcat_prueba_{}".format(datetime.date.today())
DIRECTORY_OUTPUT_FILES = "./experiments/maskcat_loop200-100"

#Preferible ruta absoluta del fichero wordlist
#WORDLIST_ROUTE = "C:\\Users\\Jorge\\Desktop\\TFG\\maskcat\\DOWNLOAD\\wordlists\\shuffled_top_1M_MD5.txt"

WORDLIST_ROUTE = "/home/alumno/maskcat/DOWNLOAD/wordlists/experiments-file_MD5.txt"


#========== Maskcat Command ==========
# Modificar los valores a corde al comando que se quiera ejecutar, no introducir máscara (se hace en hashcat_exec.py), ruta de wordlist se sextrae de
# la variable definida con anterioridad
#HASHCAT_COMMAND = "hashcat.cmd -m 0 -a 3 -d 1 --runtime=600 --status-json -O --potfile-disable --logfile-disable {}".format(WORDLIST_ROUTE)

HASHCAT_COMMAND = "NONE"

#========== Maskcat problem execution variables ==========
#MASK_LEN = Longitud de la máscara - 1
MASK_LEN=7
PREDEFINED_MASKS=0

#========== Maskcat GeneticAlgorithm execution variables ==========
GENERATIONAL = False

POPULATION_RESET = False
POPULATION_RESET_NUMBER = 1

POPULATION_SIZE=200
OFFSPRING_POPULATION =200
MAX_EVALUATIONS=20000
REPETITIONS=10

