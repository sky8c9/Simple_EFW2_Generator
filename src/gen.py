import os
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
        
    def toTxt(self, fname):
        txt = '\n'.join(self.txt_chunks)
        fpath = os.path.join(Spec.OUT, f'{fname}_efw2.txt')
        with open(fpath, 'w') as output:
            output.write(txt)
       
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
    def genSample1(self, file):
        # generate submitter record
        submitter = SubmitterRecord(file)
        self.build(submitter)

        # generate employer record
        employer = EmployerRecord(file)
        self.build(employer)

        # generate employee record
        employee = EmployeeRecord(file)
        self.build(employee)

        # generate total record & total summary
        total = TotalRecord(file)
        self.build(total, employee.record_count, employee.total)
        total.totalSummary()

        # generate final record
        fn = FinalRecord(file)
        self.build(fn, employee.record_count)

        # combine records to a single txt file
        fname = file.split('/')[-1].split('.')[0] 
        self.toTxt(fname)

    # a simple efw2 example with RA, RE, RW, RS, RT, RV & RF
    def genSample2(self, file):
        # generate submitter record
        submitter = SubmitterRecord(file)
        self.build(submitter)

        # generate employer record
        employer = EmployerRecord(file)
        self.build(employer)

        # generate employee record
        employee = EmployeeRecord(file)
        self.build(employee)

        # generate state record
        employee_state = StateRecord(file)
        self.build(employee_state)

        # generate total record & total summary
        total = TotalRecord(file)
        self.build(total, employee.record_count, employee.total)
        total.totalSummary()

        # generate state total record
        state_total = StateTotalRecord(file)
        self.build(state_total)

        # generate final record
        fn = FinalRecord(file)
        self.build(fn, employee.record_count)

        # combine records to a single txt file
        fname = file.split('/')[-1].split('.')[0] 
        self.toTxt(fname)

def run():
    if not os.path.exists(Spec.IN):
        os.makedirs(Spec.IN)

    if not os.path.exists(Spec.OUT):
        os.makedirs(Spec.OUT)

    if not os.path.exists(Spec.SUMMARY):
        os.makedirs(Spec.SUMMARY)

    for file in os.listdir(Spec.IN):
        if not file.startswith('.'):
            report = Report()
            report.genSample1(file)

if __name__ == "__main__":
    run()

    
  