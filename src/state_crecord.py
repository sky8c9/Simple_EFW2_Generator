import numpy as np
import pandas as pd
from employee_record import EmployeeRecord
from constants import Spec

class StateCRecord(EmployeeRecord):
    def __init__(self, input_file):
        super().__init__(input_file)
        self.sheet = 'RCS_RECORD'
        self.total = np.empty(0)

        # locations of amount values with len & right justify range
        self.amount_loc = [[26, 27], [39, 42], [46, 47]]
        self.default_values = {}

    def simpleCheck(self, idx):
        # reserve for asserting taxable amounts from state and city
        pass

if __name__ == "__main__":
    # Quick test on corrected state record class
    file_path = 'path to correction template file'
    state = StateCRecord(file_path)
    state.initBlock()
    state.fill()
    state.mergeBlock(Spec.SIZE)
