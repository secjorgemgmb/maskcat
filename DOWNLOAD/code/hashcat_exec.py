import subprocess
import regex
import json
import datetime
import platform

import maskcat_config

class HashcatExecution ():

    def __init__(self):
        self.OS = platform.system()
        self.wordlist = maskcat_config.WORDLIST_ROUTE

    def string_to_timestamp (self, day:str, hour:str):
    
        ISO_format_string = day+" "+hour
        date = datetime.datetime.fromisoformat(ISO_format_string)
        return date.timestamp()

    def run (self, mask):
        day_start = datetime.date.today()

        if self.OS == "Darwin":
            result = subprocess.run([r"hashcat", "-m" ,"0", "-a", "3", "--runtime=600", "--status-json", "--session={:s}".format(mask), 
            self.wordlist, "-O", "--potfile-disable", "--logfile-disable", mask], stdout=subprocess.PIPE).stdout.decode("utf-8")

        elif self.OS == "Linux":
            result = subprocess.run([r"hashcat",  "-m" ,"0", "-a", "3", "--runtime=600", "--status-json", "-d", "1", "-O", "--potfile-disable", "--logfile-disable",
            "--session={:s}".format(mask.replace("?", "_")), self.wordlist,  mask], stdout=subprocess.PIPE).stdout.decode("utf-8")
        
        elif self.OS == "Windows":
            result = subprocess.run([r"hashcat.cmd",  "-m" ,"0", "-a", "3", "--runtime=600", "--status-json", "-d", "1", "-O", "--potfile-disable", "--logfile-disable",
            "--session={:s}".format(mask.replace("?", "_")), self.wordlist,  mask], stdout=subprocess.PIPE).stdout.decode("utf-8")

        else:
            raise Exception("Operating system not defined or invalid value")

        day_stop = datetime.date.today()

        reg1 = regex.compile("{.*}")
        reg2 = regex.compile("Started: .*")
        reg3 = regex.compile("Stopped: .*")
        reg_hora = regex.compile("\d\d:\d\d:\d\d")

        filtered_result = reg1.search(result)
        resultJSON = json.loads(filtered_result[0])
        start_date_string = str(reg2.search(result)[0])
        timestamp_start = self.string_to_timestamp(str(day_start), str(reg_hora.search(start_date_string)[0]))
        stop_date_string = str(reg3.search(result)[0])
        timestamp_stop = self.string_to_timestamp(str(day_stop), str(reg_hora.search(stop_date_string)[0]))

        recovered_hashes = resultJSON["recovered_hashes"][0]

        return [-(recovered_hashes / (timestamp_stop - timestamp_start)), (timestamp_stop - timestamp_start)]

    