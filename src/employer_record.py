import numpy as np
import pandas as pd
from record import Record

class EmployerRecord(Record):
    def __init__(self, input_file):
        super().__init__(input_file)
        self.sheet = 'RE_RECORD'

        '''
        Default settings:
            + Terminating business = 0
            + Kind of employer = N
            + Employment code = R
            + Third-party sick pay indicator = 0
        '''
        self.default_values = {5:0, 15:'N', 20:'R', 22:0}

    def fill(self):
        for i in range(0, self.field_count):
            if not pd.isna(self.meta_data[1][i]):
                self.blocks[0][i] = np.chararray.ljust(str(self.meta_data[1][i]), self.meta_data[0][i])

if __name__ == "__main__":
    # Quick test on employer record class
    file_path = 'path to template file'
    employer = EmployerRecord(file_path)
    employer.initBlock()
    employer.fill()
    employer.mergeBlock()