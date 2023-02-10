import numpy as np
import pandas as pd
from record import Record
from submitter_record import SubmitterRecord
from employer_record import EmployerRecord
from employee_record import EmployeeRecord
from state_record import StateRecord
from state_total_record import StateTotalRecord
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

    # a simple efw2 example with RA, RE, RW, RT & RF
    def sample1(self):
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

    # a simple efw2 example with RA, RE, RW, RS, RT, RV & RF
    def sample2(self):
        # generate submitter record
        submitter = SubmitterRecord()
        self.build(submitter)

        # generate employer record
        employer = EmployerRecord()
        self.build(employer)

        # generate employee record
        employee = EmployeeRecord()
        self.build(employee)

        # generate state record
        employee_state = StateRecord()
        self.build(employee_state)

        # generate total record & total summary
        total = TotalRecord()
        self.build(total, employee.record_count, employee.total)
        total.totalSummary()

        # generate state total record
        state_total = StateTotalRecord()
        self.build(state_total)

        # generate final record
        fn = FinalRecord()
        self.build(fn, employee.record_count)

        # combine records to a single txt file
        self.toTxt()

if __name__ == "__main__":
    report = Report()
    
    #report.sample1()
    report.sample2()