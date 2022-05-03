import json

###
# Clase para guardar el estado devuelto por hascat al terminar la ejecución
# Se guarda todo el JSON que devuelve Hashcat por cada mascara que se utiliza
###
class HascatJSON (object):
    def __init__(self, df=None):
        self.df = json.loads("""[]""")

    def setJSON (self, s): self.df.append(s)
    def getJSON (self): return self.df

    def __str__(self):
        return json.dumps(self.df)
