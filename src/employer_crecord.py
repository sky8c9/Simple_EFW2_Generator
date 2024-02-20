import numpy as np
import pandas as pd
from employer_record import EmployerRecord
from constants import Spec

class EmployerCRecord(EmployerRecord):
    def __init__(self, input_file):
        super().__init__(input_file)
        self.sheet = 'RCE_RECORD'
        self.default_values = {}

if __name__ == "__main__":
    # Quick test on corrected employer record class
    file_path = 'path to correction template file'
    employer = EmployerCRecord(file_path)
    employer.initBlock(Spec.CIN)
    employer.fill()
    employer.mergeBlock(Spec.CSIZE)