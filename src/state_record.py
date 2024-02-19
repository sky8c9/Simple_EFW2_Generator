import numpy as np
import pandas as pd
from employee_record import EmployeeRecord
from constants import Spec

class StateRecord(EmployeeRecord):
    def __init__(self, input_file):
        super().__init__(input_file)
        self.sheet = 'RS_RECORD'
        self.total = np.empty(0)

        # locations of amount values with len & right justify
        self.amount_loc = [[20, 21], [29, 30], [33, 34]]

        '''
        Default settings:
            + State Code = 06 (See Appendix F for numeric state code)
            + Tax Type Code = C (City Income Tax)
        '''
        self.default_values = {1:'06', 28:'06', 32:'C'}

    def simpleCheck(self, idx):
        # reserve for asserting taxable amounts from state and city
        pass

if __name__ == "__main__":
    # Quick test on state record class
    file_path = 'path to template file'
    state = StateRecord(file_path)
    state.initBlock()
    state.fill()
    state.mergeBlock()
