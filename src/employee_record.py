import numpy as np
import pandas as pd
from record import Record
from constants import Spec

class EmployeeRecord(Record):
    def __init__(self):
        super().__init__()
        self.sheet = 'RW_RECORD'
        self.total = np.empty(0)

        # locations of amount values with len & right justify
        self.amount_loc = [[16, 22], [24, 29], [31, 34], [36, 42]]

        '''
        Default settings:
            + Statutory Employee Indicator = 0
            + Retirement Plan Indicator = 0
            + Third-Party Sick Pay Indicator = 0
        '''
        self.default_values = {44:0, 46:0, 47:0}

    def simpleCheck(self, idx):
        # amount on box 1 to 7
        indices = np.arange(self.amount_loc[0][0], self.amount_loc[0][1] + 1, 1)
        box_1_7 = np.take(self.meta_data[idx + Spec.DATA_OFFSET], indices).astype(float)
        box_1_7 = np.nan_to_num(box_1_7, nan=0.00)
        earning, fed_w, ss_wage, ss_tax, med_wage, med_tax, ss_tip = box_1_7
        row_idx = idx + Spec.DATA_ROW_START

        # Test amount & cap
        assert fed_w <= earning, f'Error at row#{row_idx}: Federal tax withholding is greater earning'
        assert ss_wage + ss_tip <= Spec.SS_MAX_22, f'Error at row#{row_idx}: Social wages + tip cant be greater than {Spec.SS_MAX_22}'
        assert med_wage >= ss_wage, f'Error at row#{row_idx}: Medicare wages cant be smaller than Social security wages'

        # Test tax relations & calculations accuracy
        assert ss_wage + ss_tip > ss_tax and abs((ss_wage + ss_tip) * Spec.SS_RATE_22 - ss_tax) < Spec.EPSILON, f'Error at row#{row_idx}: Social security tax is incorrect'
        assert med_wage + ss_tip > med_tax and abs((med_wage + ss_tip) * Spec.MC_RATE_22 - med_tax) < Spec.EPSILON, f'Error at row#{row_idx}: Medicare tax is incorrect'

    def fill(self):
        # extract indices of numeric fields
        numeric_indices = np.hstack(np.array([np.arange(l,r+1) for l,r in self.amount_loc], dtype=object))
        
        # mask off numeric fields among input fields 
        field_indices = np.array(np.arange(0, self.field_count))
        text_indices_mask = np.ones(field_indices.shape, bool)
        text_indices_mask[numeric_indices] = False

        # extract indices of text fields
        text_indices = field_indices[text_indices_mask] 
        
        # process input data
        self.total = np.empty(self.field_count, dtype=np.longlong)
        self.total.fill(0)
        for i in range(self.record_count):
            # process text fields
            for j in text_indices:
                if not pd.isna(self.meta_data[i + Spec.DATA_OFFSET][j]):
                    self.blocks[i][j] = np.chararray.ljust(str(self.meta_data[i + Spec.DATA_OFFSET][j]), self.meta_data[0][j])                

            # process numeric fields
            for j in numeric_indices:
                # read, reformat and assert amount value
                amount = float(self.meta_data[i + Spec.DATA_OFFSET][j])
                amount = np.nan_to_num(amount, nan=0.00)
                assert amount >= 0, f'Error at row#{i + Spec.DATA_ROW_START}: Amount is negative at column {self.column_name[j]}'

                # set amount value & add to total
                amount = np.longlong(amount * 100)
                self.blocks[i][j] = np.chararray.rjust(str(amount), self.meta_data[0][j], fillchar='0')
                self.total[j] += amount

            # assert values on w2 (box1 to box7 only)
            self.simpleCheck(i)

if __name__ == "__main__":
    # Quick test on employee record class
    employee = EmployeeRecord()
    employee.initBlock()
    employee.fill()
    employee.mergeBlock()
        