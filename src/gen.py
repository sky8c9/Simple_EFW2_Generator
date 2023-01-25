import numpy as np
import pandas as pd
from record import Record
from submitter_record import SubmitterRecord
from employer_record import EmployerRecord
from employee_record import EmployeeRecord
from total_record import TotalRecord
from final_record import FinalRecord
from constants import Spec

class Report():
    def __init__(self):
        self.txt_chunks = []
        
    def toTxt(self):
        upload_txt = '\n'.join(self.txt_chunks)
        upload_file = open(f'../{Spec.EFW2_FILE_OUT}', 'w')
        upload_file.write(upload_txt)
        upload_file.close()

    def build(self, record:Record, rw_cnt=None, total=None):
        record.initBlock()

        if isinstance(record, TotalRecord):
            record.fill(rw_cnt, total)
        elif isinstance(record, FinalRecord):
            record.fill(rw_cnt)
        else:
            record.fill()

        record.mergeBlock()
        self.txt_chunks.append('\n'.join(record.lines))

    # a simple efw2 example
    def gen(self):
        # generate submitter record
        submitter = SubmitterRecord()
        self.build(submitter)

        # generate employer record
        employer = EmployerRecord()
        self.build(employer)

        # generate employee record
        employee = EmployeeRecord()
        self.build(employee)

        # generate total record & total summary
        total = TotalRecord()
        self.build(total, employee.record_count, employee.total)
        total.totalSummary()

        # generate final record
        fn = FinalRecord()
        self.build(fn, employee.record_count)

        # combine records to a single txt file
        self.toTxt()

if __name__ == "__main__":
    report = Report()
    report.gen()