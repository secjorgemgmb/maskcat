import subprocess
import regex
import json
from data import HascatJSON

def execHashcat (data, mask):

    #hashcat -m 0 -a 3 --runtime=60 --status-json --session=[mascara para identificar] wordlists/wordlist1MD5.txt [mascara]
    result = subprocess.run(['hashcat', '-m' ,'0', '-a', '3', '--runtime=60', '--status-json', '--session={:s}'.format(mask), 
    'wordlists/wordlist1MD5.txt', mask], stdout=subprocess.PIPE).stdout.decode('utf-8')

    # RegEX para encontrar el JSON dentro de la salida obtenida de HASHACAT == grep '{.*}'
    reg1 = regex.compile('{.*}')
    
    filteredResult = reg1.search(result)
    resultJSON = json.loads(filteredResult[0])

    data.setJSON(resultJSON)

    