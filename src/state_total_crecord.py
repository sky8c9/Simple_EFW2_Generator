import numpy as np
import pandas as pd
from state_total_record import StateTotalRecord
from constants import Spec

class StateTotalCRecord(StateTotalRecord):
    def __init__(self, input_file):
        super().__init__(input_file)
        self.sheet = 'RCV_RECORD'

    def fill(self):
        # set id at block#0
        self.blocks[0][0] = np.chararray.ljust('RCV', self.meta_data[0][0])

if __name__ == "__main__":
    # Quick test on state total record class
    file_path = 'path to correction template file'
    stateTotal = StateTotalCRecord(file_path)
    stateTotal.initBlock()
    stateTotal.fill()
    stateTotal.mergeBlock(Spec.CSIZE)