import numpy as np
import pandas as pd
from submitter_record import SubmitterRecord
from constants import Spec

class SubmitterCRecord(SubmitterRecord):
    def __init__(self, input_file):
        super().__init__(input_file)
        self.sheet = 'RCA_RECORD'
        self.default_values = {}

if __name__ == "__main__":
    # Quick test on submitter record class
    file_path = 'path to correction template file'
    submitter = SubmitterCRecord(file_path)
    submitter.initBlock()
    submitter.fill()
    submitter.mergeBlock(Spec.CSIZE)
        