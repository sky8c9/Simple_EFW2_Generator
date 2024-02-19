import numpy as np
import pandas as pd
from record import Record
from employee_record import EmployeeRecord
from constants import Spec

class TotalRecord(Record):
    def __init__(self, input_file):
        super().__init__(input_file)
        self.sheet = 'RT_RECORD'

        # locations of amount values len & right justify
        self.amount_loc = [[1, 1], [2, 8], [10, 15], [17, 28]]

        # rt to rw fields location mapping
        self.rt2rw_map = {
            2:16 , 3:17 , 4:18 , 5:19 , 6:20 , 7:21 , 8:22,
            10:24 , 11:25 , 12:26 , 13:27 , 14:28 , 15:29,
            17:31, 18:32, 19:33, 20:34,
            21:41, 22:36,
            24:37, 25:38, 26:39, 27:40, 28:42
        }

    def fill(self, rw_cnt, total):
        # set id at block#0 and total record count at block#1
        self.blocks[0][0] = np.chararray.ljust('RT', self.meta_data[0][0])
        self.blocks[0][1] = np.chararray.rjust(str(rw_cnt), self.meta_data[0][1], fillchar='0')

        # transfer value from from total value collected from employee records to corresponding blocks
        for k,v in self.rt2rw_map.items():
            self.blocks[0][k] = np.chararray.rjust(str(total[v]), self.meta_data[0][k], fillchar='0')

    def totalSummary(self):
        # extract total columns from RT_RECORD
        indices = list(self.rt2rw_map.keys())
        total_titles = [self.column_name[i] for i in indices]
        total_values = [float(self.blocks[0][i]) / 100 for i in indices]

        # create summary report
        summary = pd.DataFrame(columns=total_titles)        
        summary.loc[len(summary)] = total_values

        fname = 'sample' if self.input_file == None else self.input_file.split('.')[0]
        summary.to_csv(f'{Spec.SUMMARY}/{fname}.CSV', float_format='%.2f', index=False)

if __name__ == "__main__":
    # Quick test on total record class
    file_path = 'path to template file'
    employee = EmployeeRecord(file_path)
    employee.initBlock()
    employee.fill()

    total = TotalRecord(file_path)
    total.initBlock()
    total.fill(employee.record_count, employee.total)
    total.mergeBlock()
        