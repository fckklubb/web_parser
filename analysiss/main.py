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

    a_file_root = '/Users/fckklubb/Documents/Python/web_parser/outputs/Competitors-rates-22-02-2024-19_32_30.xlsx'
    a_file = pd.ExcelFile(a_file_root)
    df = GatherAllColumns(a_file)

    df['RAIDEN'] = df['RAIDEN'].apply(lambda x: 0.85*x if not isinstance(x, str) else x)
    df.loc['IGAR_new', 'RAIDEN'] = df.loc['IGAR_new', 'RAIDEN'].apply(lambda x: (0.7/0.85)*x if not isinstance(x, str) else x)
    df.loc['IGAR_old', 'RAIDEN'] = df.loc['IGAR_old', 'RAIDEN'].apply(lambda x: (0.7/0.85)*x if not isinstance(x, str) else x)

    df['MIN'] = df.min(axis=1, numeric_only=True)
    df['DELTA'] = df['MIN']
    df.loc[[(f'{i}_{j}', f'{k}') for i in sipp_names for j in park for k in rate_names], 'DELTA'] = df.loc[[(f'{i}_{j}', f'{k}') for i in sipp_names for j in park for k in rate_names], 'RAIDEN'] - df.loc[[(f'{i}_{j}', f'{k}') for i in sipp_names for j in park for k in rate_names], 'MIN']
    # df['DELTA'] = df['RAIDEN'] - df['MIN']
    # df['DELTA %'] = round(100 * df['DELTA']/df['RAIDEN'], 2)

    df.to_excel(data_folder+'/'+'analysiss.xlsx', sheet_name='1')