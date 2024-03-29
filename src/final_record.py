import numpy as np
import pandas as pd
from record import Record
from constants import Spec

class FinalRecord(Record):
    def __init__(self, input_file):
        super().__init__(input_file)
        self.sheet = 'RF_RECORD'

    def fill(self, rw_cnt):
        # set id at block#0 and total record count at block#2
        self.blocks[0][0] = np.chararray.ljust('RF', self.meta_data[0][0])
        self.blocks[0][2] = np.chararray.rjust(str(rw_cnt), self.meta_data[0][2], fillchar='0')        

if __name__ == "__main__":
    # Quick test on final record class
    file_path = 'path to template file'
    fn = FinalRecord(file_path)
    fn.initBlock()
    fn.fill(12345)
    fn.mergeBlock()