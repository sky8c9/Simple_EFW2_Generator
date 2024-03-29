class Spec:
    # Template
    TEMPLATE_FILE = '../template/template_correction.xlsx'
    TEMPLATE_WRITE_OFFSET = 2

    # RRecord
    IN = '../in'
    OUT = '../out'
    SUMMARY = '../summary'
    SIZE = 512
    DATA_OFFSET = 1
    DATA_ROW_START = 3

    # CRecord
    CIN = '../cin'
    COUT = '../cout'
    CSIZE = 1024

    # Tax rate & cap 2024
    SS_RATE = 0.062
    SS_MAX = 168600
    MC_RATE = 0.0145    
    EPSILON = 0.2

class CRecord_Mapping:
    '''
    # mapping locations from source record to correction record
        [sl,sr,sd, tl,tr,td]
        [sl, sr): moving at rate sd
        [tr, td): moving at rate td
    ''' 

    RCA = [[1,5,1, 1,5,1], [7,8,1, 5,6,1], [19,39,1, 6,26,1]]

    RCE = [[1,2,1, 1,2,1], [2,3,1, 4,5,1], [3,4,1, 3,4,1], 
           [4,5,1, 5,6,1], [6,7,1, 6,7,1], [8,15,1, 8,15,1], 
           [15,16,1, 24,25,1], [17,20,1, 16,19,1], 
           [22,23,1, 21,22,1], [23,28,1, 25,30,1]]
    
    RCW = [[1,2,1, 1,2,1], [2,5,1, 3,6,1], [6,12,1, 9,15,1],
           [13,16,1, 16,19,1], [16,23,1, 19,33,2], [24,30,1, 34,46,2],
           [31,35,1, 49,57,2], [36,43,1, 58,72,2], [44,45,1, 73,74,1],
           [46,48,1, 75,79,2]]
    
    RCS = [[0,2,1, 0,2,1], [2,4,1, 2,6,2], [4,7,1, 6,9,1],
           [8,14,1, 12,18,1], [15,19,1, 19,24,1], [20,21,1, 26,27,1],
           [22,25,1, 28,34,2], [26,27,1, 35,36,1], [28,29,1, 38,39,1], 
           [29,31,1, 39,43,2], [31,33,1, 43,45,1], [33,34,1, 46,48,2], 
           [35,36,1, 48,49,1], [36,38,1, 50,52,1]]
  