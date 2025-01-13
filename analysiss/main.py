import numpy as np
import pandas as pd
import datetime

from sources import rates_root, matches_root, data_folder, rate_names
from config import park, sipp_names

# from Levenshtein import ratio

from funcs import *

from collections import namedtuple

T = namedtuple('T', 'sipp_names rate_names park')
Trio = T(sipp_names, rate_names, park)

if __name__ == '__main__':

    a_file_root = '../outputs/Competitors-rates-13-01-2025-11_29_51.xlsx'
    a_file = pd.ExcelFile(a_file_root)
    df = GatherAllColumns(a_file)

    sipp_list = [i+'_'+j for i in sipp_names for j in park]
    for s in sipp_list:
        # SET DISCOUNTS (are active till 17.03.2024)
        # k = 0.7 if 'IGAR' in s else 0.85
        # k = 1
        k = 1.0
        """ if 'EDMR' in s: k = 0.9 # discount = 10%
        if 'EDAR' in s: k = 0.9 # discount = 10%
        if 'HDAR' in s: k = 0.85 # discount = 15%
        if 'CWMR' in s: k = 0.85 # discount = 15%
        if 'CDAR' in s: k = 0.9 # discount = 10%
        if 'EGAR' in s: k = 0.9 # discount = 10%
        if 'HGAR' in s: k = 0.9 # discount = 10%
        if 'IGAR' in s: k = 0.6 # discount = 40%
        if 'SDAR' in s: k = 0.85 # discount = 15%
        if 'XFAR' in s: k = 0.9 # discount = 10% """
        

        # arr = ['EDAR','EGAR','HGAR','XFAR']
        # arr2 = [el in s for el in arr]
        # if np.any(arr2): k = 0.8 # discount = 20%

        df.loc[(s, rate_names), 'RAIDEN'] = k * df.loc[(s, rate_names), 'RAIDEN']
        df.loc[(s, rate_names), 'MIN'] = df.loc[(s, rate_names), :].min(axis=1)
        df.loc[(s, rate_names), 'DELTA'] = df.loc[(s, rate_names), 'RAIDEN'] - df.loc[(s, rate_names), 'MIN']
        try:
            df.loc[(s, rate_names), 'DELTA %'] = df.loc[(s, rate_names), 'DELTA']/df.loc[(s, rate_names), 'RAIDEN']
            np_a = df.loc[(s, rate_names), 'DELTA %'].to_numpy()
            np_a = 100 * np_a
            np_a = np.array(np_a, dtype=float)
            np_a = np.around(np_a, decimals=2)
            df.loc[(s, rate_names), 'DELTA %'] = np_a
        except Exception as err:
            print(err, ' has happened for', s, '!!!')
    
    #append to an existing file!
    sheet_name = datetime.datetime.today().strftime("%d-%m-%Y_@_%H_%M")
    with pd.ExcelWriter(data_folder+'/'+'analysiss.xlsx', mode='a') as writer:
        df.to_excel(writer, sheet_name=sheet_name)