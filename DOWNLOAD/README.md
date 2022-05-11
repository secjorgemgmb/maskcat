Requisitos:

  -Hashcat instalado
  
  -Python 3

Instalación del proyecto:

  1. Clonación de esta carpeta del repositorio.
  2. Ejecución del comando "pip install -r requirements.txt" para instalar los módulos necesarios presentes en el fichero requirements.txt.

Ejecución del proyecto:

  1. Configuración de los parámetros de ejecución en el fichero "maskcat_config.py"

    - La ruta del wordlist se recomienda que sea una ruta absoluta para que hashcat encuentre el fichero correctamente.
    
    - MASK_LEN debe tener el valor de la longitud deseada restandole 1.
    
    - HASHCAT_COMMAND se puede dejar en "NONE" para que detecte SO o se puede introducir el comando de hashcat que se quiere utilizar, definiendo la ruta en la variable WORDLIST_ROUTE y no introduciendo máscaras ya que se hace en hashcat_exec.py. Siempre se debe tener "--potfile-disable" para que los resultados sean correctos.
    
  2. Ejecución del fichero main.py
