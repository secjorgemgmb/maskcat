import subprocess
import regex
import json
from data import HascatJSON
import datetime


def stringToTimestamp ( dateString:str):
    months = {"Jan":'01', "Feb":'02', "Mar":'03', "Apr":'04', "May":'05', "Jun":'06', "Jul":'07',"Aug":'08', "Sep":'09', "Oct":'10', "Nov": '11', "Dec":'12'}
    ISOFormatString:str
    listDateString = dateString.rsplit(sep=' ')
    ISOFormatString = listDateString[5]+'-'+months.get(listDateString[2])+'-'+listDateString[3]+' '+listDateString[4]
    date = datetime.datetime.fromisoformat(ISOFormatString)
    return date.timestamp()

def execHashcat (mask):

    #-------------------- COMANDO EJECUCIÓN MAC --------------------------------------
    #hashcat -m 0 -a 3 --runtime=60 --status-json --session=[mascara para identificar] wordlists/wordlist1MD5.txt [mascara]
  
    result = subprocess.run(['./hashcat', '-m' ,'0', '-a', '3', '--runtime=600', '--status-json', '--session={:s}'.format(mask), 
    '/Users/jorgemartinezgarcia/OneDrive - Universidad Rey Juan Carlos/TFG/maskcat/wordlists/rockyouMD5_1.txt', '-O', '--potfile-disable', mask], stdout=subprocess.PIPE).stdout.decode('utf-8')
    
    
    #-------------------- COMANDO EJECUCIÓN WINDOWS WSL -----------------------------------
    #.\Desktop\hashcat-6.2.4\hashcat.exe -m 0 -a 3 --runtime=60 --status-json 'C:\Users\Jorge\OneDrive - Universidad Rey Juan Carlos\TFG\maskcat\wordlists\wordlist1MD5.txt' ?d?d?d?d
    #result = subprocess.run([r'.\hashcat.exe',  '-m' ,'0', '-a', '3', '--runtime=60', '--status-json', '--session={:s}'.format(mask.replace('?', '_')), 
    #r'C:\Users\Jorge\OneDrive - Universidad Rey Juan Carlos\TFG\maskcat\wordlists\wordlist1MD5.txt', mask], stdout=subprocess.PIPE).stdout.decode('utf-8')

    # RegEX para encontrar el JSON dentro de la salida obtenida de HASHACAT == grep '{.*}'
    timestampEnd = datetime.datetime.now().timestamp()

    reg1 = regex.compile('{.*}')
    reg2 = regex.compile('Started: .*')
    reg3 = regex.compile('Stopped: .*')

    filteredResult = reg1.search(result)
    resultJSON = json.loads(filteredResult[0])
    startDateString = str(reg2.search(result)[0])
    timestampStart = stringToTimestamp(startDateString)
    stopDateString = str(reg3.search(result)[0])
    timestampStop = stringToTimestamp(stopDateString)

    recoveredHashes = resultJSON['recovered_hashes'][0]

    #print(str(recoveredHashes+ ' - ') + str(timestampStart) + ' - ' + str(timestampEnd))
    #return [recoveredHashes, timestampStart, timestampEnd]
    # ó 
    return -(recoveredHashes / (timestampStop - timestampStart))

    