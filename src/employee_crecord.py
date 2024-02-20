import numpy as np
import pandas as pd
from employee_record import EmployeeRecord
from constants import Spec

class EmployeeCRecord(EmployeeRecord):
    def __init__(self, input_file):
        super().__init__(input_file)
        self.sheet = 'RCW_RECORD'
        
        # locations of amount values with len & right justify
        self.amount_loc = [[19, 32], [34, 47], [49, 56], [58, 71]]

        # default values
        self.default_values = {}

    def extract_box_1_7(self, data):
        # extract box 1 - 7 corrected values
        indices = np.arange(self.amount_loc[0][0] + 1, self.amount_loc[0][1] + 2, 2)
        box_1_7 = np.take(data, indices).astype(float)
        box_1_7 = np.nan_to_num(box_1_7, nan=0.00)
        return box_1_7

if __name__ == "__main__":
    # Quick test on employee record class
    file_path = 'path to correction template file'
    employee = EmployeeCRecord(file_path)
    employee.initBlock()
    employee.fill()
    employee.mergeBlock(Spec.CSIZE)
        