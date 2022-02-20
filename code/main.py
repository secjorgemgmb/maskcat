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

    # masks = ['?s?d?u?s?l?s', '?s?u?s?u?u?s?l','?s?u?s?u?u?l','?u?s?d?l?u','?d?l?u?l?u?l?l','?l?u?s?d?u?s?l','?d?s?d?d?u','?s?l?l?u?d','?u?d?l?l?d?l?s','?u?s?d?s?s?l?u']
    
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
    
