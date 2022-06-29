#========== Maskcat problem execution variables ==========
# Longitud de las máscaras que se desean comprobar. Si se quieren máscaras de longitud 8, indicarlo con valor 7 (longitud deseada - 1)
MASK_LEN=7
MUTATION_PROB = 0.1
CROSSOVER_PROB = 0.7

# True si se quiere utilizar el AG generacional - False si se quiere el AG clásico
GENERATIONAL = False

POPULATION_SIZE=300
GENERATION_NUMBER = 100
REPETITIONS=1

#========== Directories to open or write files ==========
# True si se quieren ficheros de salida - False si no se quieren ficheros de salida
OUTPUT_FILES = True
DIRECTORY_OUTPUT_FILES = "./experiments/maskcat_population300-generations100"

#Preferible ruta absoluta del fichero wordlist ejemplos: 
# C:\\Users\\USER\\maskcat\\wordlists\\experiments-file_MD5.txt
# /home/USER/maskcat/wordlists/experiments-file_MD5.txt
WORDLIST_ROUTE = "C:\\Users\\Jorge\\Desktop\\TFG\\maskcat\\wordlists\\experiments-file_MD5.txt"


#========== Maskcat Command ==========
# Modificar los valores a corde al comando que se quiera ejecutar, no introducir máscara (se hace en hashcat_exec.py), ruta de wordlist se sextrae de
# la variable definida con anterioridad. En caso de querer el que se especifica en fichero hashcat_exe.py introducir NONE como valor
# Ejemplo comando: "hashcat.cmd -m 0 -a 3 -d 1 --runtime=600 --status-json -O --potfile-disable --logfile-disable {}".format(WORDLIST_ROUTE)
HASHCAT_COMMAND = "NONE"





PREDEFINED_MASKS=0

