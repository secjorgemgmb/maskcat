Requisitos:

  -Hashcat instalado
  
  -Python 3

Instalación del proyecto:

  1. Clonación de esta carpeta del repositorio.
  2. Ejecución del comando "pip install -r requirements.txt" para instalar los módulos necesarios presentes en el fichero requirements.txt.

Ejecución del proyecto:
  1. Moverse a la carpeta "DOWNLOAD/code" del proyecto

  2. Configuración de los parámetros de ejecución en el fichero "maskcat_config.py"

    - Establecer la ruta del wordlist de cadenas cifradas en formato absoluto (/home/user/maskcat/DOWNLOAD/wordlists/wordlist.txt)
    
    - Establecer tamaño de población y tamaño de offspring (el mismo valor); además establecer el número máximo de evaluaciones (MAX_EVALUATIONS = POPULATION_SIZE * NUMERO_GENERACIONES_DESEADO)
    
    - Si se quiere que sea generacional, establecer GENERATIONAL a True.
    
    - Si se quiere que sea con reseteo de población, establecer POPULATION_RESET a True y POPULATION_RESET_NUMBER al valor de las n generaciones que se quiere que se resetee la poblacion.
    
    - MASK_LEN debe tener el valor de la longitud deseada restandole 1.
    
    - HASHCAT_COMMAND se puede dejar en "NONE" para que detecte SO o se puede introducir el comando de hashcat que se quiere utilizar, definiendo la ruta en la variable WORDLIST_ROUTE y no introduciendo máscaras ya que se hace en hashcat_exec.py. Siempre se debe tener "--potfile-disable" para que los resultados sean correctos.
    
  3. Ejecución del fichero main.py con "python3 main.py"
