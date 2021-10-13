import subprocess
import regex
import json
from data import HascatJSON
import datetime

def execHashcat (mask):

    #-------------------- COMANDO EJECUCIÓN MAC --------------------------------------
    #hashcat -m 0 -a 3 --runtime=60 --status-json --session=[mascara para identificar] wordlists/wordlist1MD5.txt [mascara]
  
    result = subprocess.run(['./hashcat', '-m' ,'0', '-a', '3', '--runtime=600', '--status-json', '--session={:s}'.format(mask), 
    '/Users/jorgemartinezgarcia/OneDrive - Universidad Rey Juan Carlos/TFG/maskcat/wordlists/rockyouMD5_1.txt', mask], stdout=subprocess.PIPE).stdout.decode('utf-8')
    
    
    #-------------------- COMANDO EJECUCIÓN WINDOWS WSL -----------------------------------
    #.\Desktop\hashcat-6.2.4\hashcat.exe -m 0 -a 3 --runtime=60 --status-json 'C:\Users\Jorge\OneDrive - Universidad Rey Juan Carlos\TFG\maskcat\wordlists\wordlist1MD5.txt' ?d?d?d?d
    #result = subprocess.run([r'.\hashcat.exe',  '-m' ,'0', '-a', '3', '--runtime=60', '--status-json', '--session={:s}'.format(mask.replace('?', '_')), 
    #r'C:\Users\Jorge\OneDrive - Universidad Rey Juan Carlos\TFG\maskcat\wordlists\wordlist1MD5.txt', mask], stdout=subprocess.PIPE).stdout.decode('utf-8')

    # RegEX para encontrar el JSON dentro de la salida obtenida de HASHACAT == grep '{.*}'
    timestampEnd = datetime.datetime.now().timestamp()

    reg1 = regex.compile('{.*}')
    
    filteredResult = reg1.search(result)
    resultJSON = json.loads(filteredResult[0])
    timestampStart = resultJSON['time_start']
    recoveredHashes = resultJSON['recovered_hashes'][0]

    #print(str(recoveredHashes+ ' - ') + str(timestampStart) + ' - ' + str(timestampEnd))



    #return [recoveredHashes, timestampStart, timestampEnd]
    # ó 
    return recoveredHashes / (timestampEnd - timestampStart)

    