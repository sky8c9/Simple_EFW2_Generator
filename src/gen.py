import os, shutil
import numpy as np
import pandas as pd
from constants import Spec, CRecord_Mapping

from record import Record
from submitter_record import SubmitterRecord
from employer_record import EmployerRecord
from employee_record import EmployeeRecord
from state_record import StateRecord
from state_total_record import StateTotalRecord
from total_record import TotalRecord
from final_record import FinalRecord

from submitter_crecord import SubmitterCRecord
from employer_crecord import EmployerCRecord
from employee_crecord import EmployeeCRecord
from state_crecord import StateCRecord
from state_total_crecord import StateTotalCRecord
from total_crecord import TotalCRecord
from final_crecord import FinalCRecord

class Report():
    def __init__(self, inDir, outDir, record_length):
        self.input_dir = inDir
        self.output_dir = outDir
        self.rlen = record_length
        self.txt_chunks = []
        
    def toTxt(self, fname):
        txt = '\n'.join(self.txt_chunks)
        fpath = os.path.join(self.output_dir, f'{fname}_efw2.txt')
        with open(fpath, 'w') as output:
            output.write(txt)
       
    def build(self, record:Record, rw_cnt=None, total=None):
        record.initBlock(self.input_dir)

        if isinstance(record, TotalRecord) or isinstance(record, TotalCRecord):
            record.fill(rw_cnt, total)
        elif isinstance(record, FinalRecord) or isinstance(record, FinalCRecord):
            record.fill(rw_cnt)
        else:
            record.fill()

        record.mergeBlock(self.rlen)
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

    def correctionSample(self, file):
         # generate corrected submitter record
        submitter = SubmitterCRecord(file)
        self.build(submitter)

        # generate corrected employer record
        employer = EmployerCRecord(file)
        self.build(employer)

        # generate corrected employee record
        employee = EmployeeCRecord(file)
        self.build(employee)

        # generate corrected total record & total summary
        total = TotalCRecord(file)
        self.build(total, employee.record_count, employee.total)

        # generate corrected final record
        fn = FinalCRecord(file)
        self.build(fn, employee.record_count)

        # combine records to a single txt file
        fname = file.split('/')[-1].split('.')[0] 
        self.toTxt(fname)

def clone(file):
    # create corresponding correction template file
    cfile_path = f'{Spec.CIN}/correction_{file}'
    shutil.copy(f'{Spec.TEMPLATE_FILE}', cfile_path)

    # read data from sheets
    source_sheets = pd.read_excel(f'{Spec.IN}/{file}', sheet_name=None)
    target_sheets = pd.read_excel(cfile_path, sheet_name=None)
    
    # copy data from source to correction template
    for sheet_name, sheet_data in source_sheets.items():
        target_sheet_name = f'{sheet_name[0]}C{sheet_name[1:]}'
        target_record_name = f'{sheet_name[0]}C{sheet_name[1]}'

        # skip record which is the result of other record
        if (target_record_name == 'RCF' or target_record_name == 'RCT' or target_record_name == 'RCV'):
            continue

        # obtain source data without length specification
        source = sheet_data.fillna('').to_numpy()[1:] 

        # create target
        height = len(source)
        width= len(target_sheets[target_sheet_name].columns)
        target = np.empty([height, width], dtype=object)
        target[:, 0] = target_record_name

        # map data and save to target template
        for i in range(len(source)):
            for sl, sr, sd, tl, tr, td in getattr(CRecord_Mapping, target_record_name):
                np.put(target[i], np.arange(tl, tr, td), source[i][sl:sr:sd])

        # append record to correction file
        df = pd.DataFrame(target)
        with pd.ExcelWriter(cfile_path, mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, sheet_name=target_sheet_name, header=None, startrow=Spec.TEMPLATE_WRITE_OFFSET, index=False)

def menu():
    print("-----------------------------")
    print("1: EFW2")
    print("2: EFWC2")
    print("-----------------------------")

def createReportFolders():
    # regular record IO
    if not os.path.exists(Spec.IN):
        os.makedirs(Spec.IN)

    if not os.path.exists(Spec.OUT):
        os.makedirs(Spec.OUT)

    # corrected record IO
    if not os.path.exists(Spec.CIN):
        os.makedirs(Spec.CIN)

    if not os.path.exists(Spec.COUT):
        os.makedirs(Spec.COUT)

    # summary folder for RT & RCT records
    if not os.path.exists(Spec.SUMMARY):
        os.makedirs(Spec.SUMMARY)

def run():
    # build report folders
    createReportFolders()

    # process input file
    menu()
    option = int(input("Select: "))
    report_df = [Spec.IN, Spec.OUT, Spec.SIZE] if option == 1 else [Spec.CIN, Spec.COUT, Spec.CSIZE]
    inDir, outDir, sz = report_df
    for file in os.listdir(inDir):
        if not file.startswith('.'):
            if (option == 1): # process regular record and clone its data to a corresponding correction template
                report = Report(inDir, outDir, sz)
                clone(file)
                report.genSample1(file)
            elif (option == 2): # process correction record
                report = Report(inDir, outDir, sz)
                report.correctionSample(file)

if __name__ == "__main__":
    run()