import numpy as np
import pandas as pd
from abc import abstractclassmethod
from constants import Spec

class Record():
    def __init__(self, input_file):
        # define fields
        self.input_file = input_file
        self.sheet = 'null'
        self.field_count = 0
        self.amount_loc = []
        self.default_values = {}
        self.lines = []

    def initBlock(self, input_path=Spec.IN):
        # read meta data from input sheet - record data has length of at least 1
        data = pd.read_excel(f'{input_path}/{self.input_file}', sheet_name=self.sheet, dtype=str)
        self.column_name = list(data.head())
        
        # store meta data
        self.meta_data = data.to_numpy()
        self.meta_data[0] = self.meta_data[0].astype(int)

        # record tracking variables
        self.field_count = len(self.meta_data[0])
        self.record_count = max(1, len(self.meta_data) - 1)

        # initialize record blocks
        self.blocks = np.empty([self.record_count, self.field_count], dtype=object)
        for i in range(self.record_count):
            # init blocks
            for j in range(0, self.field_count):
                self.blocks[i][j] = np.chararray(self.meta_data[0][j])
                self.blocks[i][j][:] = ' '

                # set amount blocks with defined length & right justify - range [l, r] closed interval
                for l,r in self.amount_loc:
                    if (j >= l and j <= r):
                        self.blocks[i][j] = np.chararray.zfill('', self.meta_data[0][j])

        # set default value for a record
        for i in range(self.record_count):
            for k,v in self.default_values.items():
                self.blocks[i][k] = v
    
    @abstractclassmethod
    def fill(self):
        pass

    def mergeBlock(self, record_size=Spec.SIZE):
        # process each record block
        for i in range(self.record_count):
            sequence = ''.join(np.hstack(self.blocks[i]))
            assert len(sequence) == record_size, f'one of {self.sheet} length is not matched desired length {record_size}'
            self.lines.append(sequence)