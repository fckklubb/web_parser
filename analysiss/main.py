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

    df['RAIDEN'] = 0.85 * df['RAIDEN']
    df.loc['IGAR_new', 'RAIDEN'] = (0.7/0.85) * df.loc['IGAR_new', 'RAIDEN'].to_numpy()
    df.loc['IGAR_old', 'RAIDEN'] = (0.7/0.85) * df.loc['IGAR_old', 'RAIDEN'].to_numpy()

    df['MIN'] = df.min(axis=1, numeric_only=True)
    df['DELTA'] = df['RAIDEN'] - df['MIN']
    df['DELTA %'] = round(100 * df['DELTA']/df['RAIDEN'], 2)

    df.to_excel(data_folder+'/'+'analysiss.xlsx', sheet_name='1')