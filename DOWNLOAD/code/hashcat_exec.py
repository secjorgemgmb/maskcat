import subprocess
import regex
import json
import datetime
import platform
import copy

import maskcat_config

class HashcatExecution ():

    def __init__(self):
        self.OS = platform.system()
        self.hashcat_command = self.command_definition()

    def string_to_timestamp (self, day:str, hour:str):
    
        ISO_format_string = day+" "+hour
        date = datetime.datetime.fromisoformat(ISO_format_string)
        return date.timestamp()

    def command_definition(self):
        if maskcat_config.HASHCAT_COMMAND != "NONE":
            return maskcat_config.HASHCAT_COMMAND.split()

        if self.OS == "Darwin":
            return list(["hashcat", "-m" ,"0", "-a", "3", "--runtime=600", "--status-json", maskcat_config.WORDLIST_ROUTE, "-O", "--potfile-disable", "--logfile-disable"])
        elif self.OS == "Linux":
            return list(["hashcat",  "-m" ,"0", "-a", "3", "--runtime=600", "--status-json", "-d", "1", "-O", "--potfile-disable", "--logfile-disable",maskcat_config.WORDLIST_ROUTE])
        
        elif self.OS == "Windows":
            return list(["hashcat.cmd",  "-m" ,"0", "-a", "3", "--runtime=600", "--status-json", "-d", "1", "-O", "--potfile-disable", "--logfile-disable",maskcat_config.WORDLIST_ROUTE])

        else:
            raise Exception("Operating system not defined or invalid value")


    def run (self, mask):
        # day_start = datetime.date.today()
        cmd_line = self.hashcat_command.copy()
        cmd_line.append(mask)

        timestamp_start = datetime.datetime.now()
        result = subprocess.run(cmd_line, stdout=subprocess.PIPE).stdout.decode("utf-8")
        timestamp_stop = datetime.datetime.now()
        total_seconds = (timestamp_stop - timestamp_start).total_seconds()

        reg1 = regex.compile("{.*}")
        filtered_result = reg1.search(result)
        resultJSON = json.loads(filtered_result[0])
        recovered_hashes = resultJSON["recovered_hashes"][0]

        return [-(recovered_hashes / total_seconds), recovered_hashes, total_seconds]


    
