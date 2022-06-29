# Maskcat

Makscat es un programa que mediante el uso de algoritmos genéticos optimiza la generación de patrones de *Hashcat*. En este fichero se pueden encontrar los requisitos de instalación y el método de uso.

## Requisitos de instalación

Para el correcto funcionamiento se necesitan tener instaladas las versiones que se especifican o superiores. En caso de que sean anteriores, no se asegura el correcto funcionamiento.

### Maskcat

Clonación de este repositorio.

### Hashcat

> Versión 6.2.4 o superior

Además también es necesario poder ejecutar *Hashcat* desde la carpeta del repositorio clonado.\
Si se trabaja con un sistema operativo Windows, se debe añadir el directorio al entorno del PATH. Además se debe incluir el fichero ***hashcat.cmd*** en el directorio donde se encuentra *Hashcat*, modificando el primer *cd* por el PATH del directorio donde se encuentra hashcat.

>La linea que se debe modificar es **cd TU_DIRECTORIO** donde se debe sustituir **TU_DIRECTORIO** por el PATH del directorio de Hashcat.

### Python

> Versión 3.8.10 o superior

#### Liberías de Python

Las librerías de Python que se necesitan instalar se encuentran en el fichero ***requirements.txt*** junto a las versiones de estas. Para su instalación se debe ejecutar el siguiente comando:

> pip install -r requirements.txt 


## Métodos de uso

Maskcat cuenta con un fichero de configuración llamado ***maskcat_config.py***. Este fichero tiene las siguientes variables:

> MASK_LEN= Longitud de las máscaras que se desean comprobar. Si se quieren máscaras de longitud 8, indicarlo con valor 7 (longitud deseada - 1)
>MUTATION_PROB = Probabilidad de mutación. Introducir en formato float. Por defecto valor = 0.1
>CROSSOVER_PROB = Probabilidad de cruce. Introducir en formato float. Por defecto valor = 0.7
>
> GENERATIONAL = True si se quiere utilizar el AG generacional - False si se quiere el AG clásico
> POPULATION_SIZE= Tamaño de la población
> GENERATION_NUMBER = Número de generaciones
> REPETITIONS= Número de repeticiones del algoritmo con la misma configuración. Si es mayor a 1 se obtienen estadísticas.
>
> OUTPUT_FILES = True si se quieren ficheros de salida - False si no se quieren ficheros de salida
> DIRECTORY_OUTPUT_FILES = Directorio donde se generan los ficheros de salida
> 
> WORDLIST_ROUTE = Ruta donde se encuentra el fichero de hashes. Preferible ruta completa. Ejemplos:
>   C:\\Users\\USER\\maskcat\\wordlists\\experiments-file_MD5.txt
>   /home/USER/maskcat/wordlists/experiments-file_MD5.txt
>
> HASHCAT_COMMAND = Comando que se desea ejecutar si es diferente del comando predefinido en **hashcat_exec.py**. En caso de que se quiera ejecutar el comando por defecto introducir "NONE".
> Ejemplo valor de variable: "hashcat.cmd -m [codigo hashcat] -a [codigo hashcat] -d 1 --runtime=600 --status-json -O --potfile-disable --logfile-disable >{}".format(WORDLIST_ROUTE)
> Sustituir los valores que se encuentran entre corchetes. Si no se tiene un dispositivo específico eliminar "-d 1" de la cadena

Para la configuración de los experimentos, se deben establecer los valores deseados en dicho fichero.\
En caso de que *Hashcat* no reconozca dispositivos se debe eliminar también del fichero ***hashcat_exec.py*** en las líneas 29 y 31 los valores de la lista "-d" y "1".

### Ejecución

Para ejecutar Maskcat, se debe estar en el terminal dentro del repositorio clonado. Una vez se está dentro y se ha configurado el experimento, se debe ejecutar el siguiente comando:

> python3 code/main.py

Si la configuración es la misma pero se quiere cambiar el valor de la población y generaciones, se puede ejecutar el siguiente comando:

> python3 code/main.py [población] [generaciones]

Destacar que con este uso, si se tiene activada la generación de ficheros, el directorio que se generará será *experiments/maskcat_poblacion[tamaño población]-generaciones[numero generaciones]* en caso de que se desee otro nombre, se debe modificar la línea 10 del fichero ***main.py***

## Experimentos

La carpeta ***experiments*** que se puede encontrar en el repositorio contiene todos los experimentos realizados para este Trabajo de Fin de Grado. Si no se quieren consultar se pueden eliminar.


## Autores
**Estudiante:** Jorge Martínez García (Ingeniería de la Ciberseguridad - URJC)
**Directores:** Jose Manuel Colmenar Verdugo (URJC) y Raúl Martín Santamaría (URJC)