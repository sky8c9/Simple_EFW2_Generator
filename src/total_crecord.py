import numpy as np
import pandas as pd
from total_record import TotalRecord
from employee_crecord import EmployeeCRecord
from constants import Spec

class TotalCRecord(TotalRecord):
    def __init__(self, input_file=f'../Correction_Template/ABC_template_correction.xlsx'):
        super().__init__(input_file)
        self.sheet = 'RCT_RECORD'

        # locations of amount values len & right justify
        self.total_block_size = 15
        self.amount_loc = []
        self.rcw2rct_mapping = [[19,33, 2,16], [34,48, 17,31], [49,57, 32,40], [58,72, 41,55]]

    def fill(self, rw_cnt, total_record):
        # set id at block#0 and total record count at block#1
        self.blocks[0][0] = np.chararray.ljust('RCT', self.meta_data[0][0])
        self.blocks[0][1] = np.chararray.rjust(str(rw_cnt), self.meta_data[0][1], fillchar='0')

        # transfer value from from total value collected from employee records to corresponding blocks
        total_record = total_record.astype(str)
        for rcwL, rcwR, rctL, rctR in self.rcw2rct_mapping:
            total_blocks = np.chararray.rjust(total_record[rcwL:rcwR], self.total_block_size, fillchar='0')
            np.put(self.blocks[0], np.arange(rctL, rctR), [total_blocks])

if __name__ == "__main__":
    # Quick test on total record class
    file_path = 'path to correction template file'
    employee = EmployeeCRecord(file_path)
    employee.initBlock()
    employee.fill()

    total = TotalCRecord(file_path)
    total.initBlock()
    total.fill(employee.record_count, employee.total)
    total.mergeBlock(Spec.CSIZE)
        