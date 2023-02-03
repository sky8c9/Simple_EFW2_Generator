import numpy as np
import pandas as pd
from record import Record
from constants import Spec

class StateTotalRecord(Record):
    def __init__(self):
        super().__init__()
        self.sheet = 'RV_RECORD'

    def fill(self):
        # set id at block#0
        self.blocks[0][0] = np.chararray.ljust('RV', self.meta_data[0][0])

if __name__ == "__main__":
    # Quick test on state total record class
    stateTotal = StateTotalRecord()
    stateTotal.initBlock()
    stateTotal.fill()
    stateTotal.mergeBlock()