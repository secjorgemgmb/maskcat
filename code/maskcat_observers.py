from fileinput import filename
import logging
import os
from pathlib import Path
from typing import List, TypeVar

from jmetal.core.observer import Observer

LOGGER = logging.getLogger('jmetal')

class MaskcatObserver(Observer):

    def __init__(self, directory:str, fileName:str, frequency: float = 1.0) -> None:
        """ Show the number of evaluations, best fitness and computing time.

        :param frequency: Display frequency. """
        self.display_frequency = frequency
        self.directory = directory
        self.file = fileName

        if not Path(self.directory).is_dir():
            LOGGER.warning('Directory {} does not exist. Creating it.'.format(self.directory))
            Path(self.directory).mkdir(parents=True)
        else:
            if not self.file in os.listdir(self.directory):
                fd = open("{}/{}".format(self.directory, self.file), "a")
                fd.write("Evaluations;BestFitness;SolutionArray\n")
                fd.close()

    def update(self, *args, **kwargs):
        evaluations = kwargs['EVALUATIONS']
        solutions = kwargs['SOLUTIONS']

        fd = open("{}/{}".format(self.directory, self.file), "a")
        
        if (evaluations % self.display_frequency) == 0 and solutions:

            fitness = -solutions.objectives[0]
            solutionArray = solutions.variables

            fd.write(
                '{};{};{}\n'.format(
                    evaluations, fitness, solutionArray
                )
            )
        fd.close()
