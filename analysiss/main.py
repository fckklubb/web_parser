import numpy as np
import pandas as pd

from sources import rates_root, matches_root, data_folder, rate_names
from config import park, sipp_names

# from Levenshtein import ratio

from funcs import *

from collections import namedtuple

T = namedtuple('T', 'sipp_names rate_names park')
Trio = T(sipp_names, rate_names, park)

if __name__ == '__main__':

    a_file_root = '/Users/fckklubb/Documents/Python/web_parser/outputs/Competitors-rates-01-03-2024-22_48_57.xlsx'
    a_file = pd.ExcelFile(a_file_root)
    df = GatherAllColumns(a_file)

    sipp_list = [i+'_'+j for i in sipp_names for j in park]
    for s in sipp_list:
        k = 0.7 if 'IGAR' in s else 0.85
        k = 1
        df.loc[(s, rate_names), 'RAIDEN'] = k * df.loc[(s, rate_names), 'RAIDEN']
        df.loc[(s, rate_names), 'MIN'] = df.loc[(s, rate_names), :].min(axis=1)
        df.loc[(s, rate_names), 'DELTA'] = df.loc[(s, rate_names), 'RAIDEN'] - df.loc[(s, rate_names), 'MIN']
        try:
            df.loc[(s, rate_names), 'DELTA %'] = df.loc[(s, rate_names), 'DELTA']/df.loc[(s, rate_names), 'RAIDEN']
            df.loc[(s, rate_names), 'DELTA %'] = 100 * df.loc[(s, rate_names), 'DELTA %'].to_numpy()
            # round ?!?!?
        except ZeroDivisionError:
            pass
    
    df.to_excel(data_folder+'/'+'analysiss.xlsx', sheet_name='1')