import os
import subprocess
import pandas as pd

from data import HascatJSON
from exec import execHashcat

if __name__=="__main__":
    
    dataList = HascatJSON()
    masks = ['?d?d?d?d', '?l?l?l?l']

    for mask in masks:
        execHashcat(dataList, mask)
        # Eliminar este archivo para que haga el proceso desde 0 con cada máscara, sino recovered_hashes tiene el valor total que se han 
        # recuperado con todas las máscaras usadas
        if os.path.isfile('~/.hashcat/hashcat.potfile'):
            subprocess.run(['rm', '~/.hashcat/hashcat.potfile'])
    
    dataFrame = pd.DataFrame.from_dict(dataList.getJSON())

    print('Hashcat status: 3 (running) 5 (exhausted) 6 (cracked)')
    print('--------------------------------')
    print(dataFrame)
    print(dataFrame.to_csv())

