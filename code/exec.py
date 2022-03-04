import subprocess
import regex
import json
from data import HascatJSON
import datetime


def stringToTimestamp (day:str, hour:str):
    
    ISOFormatString = day+" "+hour
    date = datetime.datetime.fromisoformat(ISOFormatString)
    return date.timestamp()

def execHashcat (mask):
    dayStart = datetime.date.today()

    #-------------------- COMANDO EJECUCIÓN MAC --------------------------------------
    #hashcat -m 0 -a 3 --runtime=60 --status-json --session=[mascara para identificar] wordlists/wordlist1MD5.txt [mascara]
  
    result = subprocess.run([r"./hashcat", "-m" ,"0", "-a", "3", "--runtime=600", "--status-json", "--session={:s}".format(mask), 
    r"maskcat/wordlists/top_1M_MD5.txt", "-O", "--potfile-disable", "--logfile-disable", mask], stdout=subprocess.PIPE).stdout.decode("utf-8")
    
    
    #-------------------- COMANDO EJECUCIÓN WINDOWS WSL -----------------------------------
    #.\Desktop\hashcat-6.2.4\hashcat.exe -m 0 -a 3 --runtime=60 --status-json "C:\Users\Jorge\OneDrive - Universidad Rey Juan Carlos\TFG\maskcat\wordlists\wordlist1MD5.txt" ?d?d?d?d
    # result = subprocess.run([r"./hashcat.exe",  "-m" ,"0", "-a", "3", "--runtime=600", "--status-json", "--session={:s}".format(mask.replace("?", "_")), 
    # r"../wordlists/top_1M_MD5.txt", "-d", "1", "-O", "--potfile-disable", "--logfile-disable", mask], stdout=subprocess.PIPE).stdout.decode("utf-8")

    # RegEX para encontrar el JSON dentro de la salida obtenida de HASHACAT == grep "{.*}"
    dayStop = datetime.date.today()

    reg1 = regex.compile("{.*}")
    reg2 = regex.compile("Started: .*")
    reg3 = regex.compile("Stopped: .*")
    regHora = regex.compile("\d\d:\d\d:\d\d")

    filteredResult = reg1.search(result)
    resultJSON = json.loads(filteredResult[0])
    startDateString = str(reg2.search(result)[0])
    timestampStart = stringToTimestamp(str(dayStart), str(regHora.search(startDateString)[0]))
    stopDateString = str(reg3.search(result)[0])
    timestampStop = stringToTimestamp(str(dayStop), str(regHora.search(stopDateString)[0]))

    recoveredHashes = resultJSON["recovered_hashes"][0]

    #print(str(recoveredHashes+ " - ") + str(timestampStart) + " - " + str(timestampEnd))
    #return [recoveredHashes, timestampStart, timestampEnd]
    # ó 
    return -(recoveredHashes / (timestampStop - timestampStart))

    