import os
import subprocess
import pandas as pd
#import jmetalpy

from exec import execHashcat
#from jMetalPy_maskcat import MaskcatSolution, MaskcatProblem


if __name__=="__main__":
    
    """ masksDictionary = {
        "mask" : [],
        "puntuation" : []
    } """
    #Implementación de diccionario cada mascara es la clave y el valor
    #es la puntuación de la máscara
    masksDictionary = {}

    masks = ['?d?d?d?d?d?d', '?l?l?l?l?l']
    
    for mask in masks:
        sol = execHashcat(mask)
        """masksDictionary['mask'].append(mask)
        masksDictionary['puntuation'].append(sol) """

        #Segunda forma de implementar
        masksDictionary[mask] = sol

        # Eliminar este archivo para que haga el proceso desde 0 con cada máscara, sino recovered_hashes tiene el valor total que se han 
        # recuperado con todas las máscaras usadas (SOLO BORRA EN WINDOWS DE MOMENTO)
        '''if os.path.isfile('hashcat.potfile'):
            os.remove('hashcat.potfile')'''
    
    for key, value in masksDictionary.items():
        print(key + ' -> ' + str(value))
    
