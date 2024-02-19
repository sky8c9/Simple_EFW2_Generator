import numpy as np
import pandas as pd
from record import Record

class SubmitterRecord(Record):
    def __init__(self, input_file):
        super().__init__(input_file)
        self.sheet = 'RA_RECORD'

        '''
        Default settings:
            + Resub indicator = 0
            + Software code = 98
            + Preparer code = L
        '''
        self.default_values = {5:0, 7:98, 38:'L'}

    def fill(self):
        for i in range(0, self.field_count):
            if not pd.isna(self.meta_data[1][i]):
                self.blocks[0][i] = np.chararray.ljust(str(self.meta_data[1][i]), self.meta_data[0][i])

if __name__ == "__main__":
    # Quick test on submitter record class
    file_path = 'path to template file'
    submitter = SubmitterRecord(file_path)
    submitter.initBlock()
    submitter.fill()
    submitter.mergeBlock()
        