import numpy as np
import pandas as pd
from final_record import FinalRecord
from constants import Spec

class FinalCRecord(FinalRecord):
    def __init__(self, input_file):
        super().__init__(input_file)
        self.sheet = 'RCF_RECORD'

    def fill(self, rw_cnt):
        # set id at block#0 and total record count at block#2
        self.blocks[0][0] = np.chararray.ljust('RCF', self.meta_data[0][0])
        self.blocks[0][1] = np.chararray.rjust(str(rw_cnt), self.meta_data[0][1], fillchar='0')        

if __name__ == "__main__":
    # Quick test on corrected final record class
    file_path = 'path to correction template file'
    fn = FinalCRecord(file_path)
    fn.initBlock()
    fn.fill(12345)
    fn.mergeBlock(Spec.CSIZE)