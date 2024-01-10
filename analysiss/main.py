import numpy as np
import pandas as pd

from sources import rates_root, matches_root, data_folder

def getRatesMatches():
    __rates_file = pd.ExcelFile(rates_root)
    __rates_sheets = __rates_file.sheet_names
    __matches_file = pd.ExcelFile(matches_root)
    
    rates_new: pd.DataFrame
    rates_old: pd.DataFrame
    matches: pd.DataFrame

    rates_new = pd.read_excel(__rates_file, "new", index_col=0, usecols=[0,1]+list(range(3, 18)), skiprows=lambda x: x not in [3]+list(range(6, 12))+list(range(17, 23)))
    rates_old = pd.read_excel(__rates_file, "old", index_col=0, usecols=[0,1]+list(range(3, 18)), skiprows=lambda x: x not in [3]+list(range(6, 12))+list(range(17, 23)))

    matches = pd.read_excel(__matches_file, index_col=0)

    return (rates_new, rates_old, matches)

if __name__ == '__main__':
    RN, RO, M = getRatesMatches()
    # print(M)

    test_sipp = input('What car?\n')

    N_or_O = lambda x: RN if x == 'new' else RO
    D = N_or_O(M.loc[test_sipp, 'park'])
    s = D[
            D[D.columns[0]]=='Lim'
            ].loc[
            'R3',
            M.loc[test_sipp, 'inp_sipp']
        ]

    print(s)