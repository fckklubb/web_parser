import pandas as pd
import numpy as np
#from Levenshtein import ratio

from sources import rate_names, rates_root, matches_root
from config import park, sipp_names

from collections import namedtuple
T = namedtuple('T', 'sipp_names rate_names park')
Trio = T(sipp_names, rate_names, park)

def BuildOneColumn(name: str, data: pd.DataFrame) -> pd.Series:
    # print('We are in the BuildOneColumn func for: ', name)
    result = GetTemplate_S(name, Trio)
    if not data.empty:
        for x in data:
            sipp = FindMatchedCar(x)
            # print('In the company: <', name, '> the SIPP code = <', sipp, '> stands for the car: ', x)
            if (sipp != 'nope') & (sipp in result.index.get_level_values('sipp')):
                # print('+++++> Adding data: ', data[x].to_numpy(), 'for the car: ', x)
                if result[sipp].isna().any():
                    result[sipp] = data[x].to_numpy()
                else:
                    rr = result[sipp].reset_index(drop=True) > data[x].reset_index(drop=True)
                    if rr.any(): # OR ALL ?!?!
                        result[sipp] = data[x].to_numpy()

    return result

def GatherAllColumns(excel_file: pd.ExcelFile):
    result = GetTemplate_DF(Trio)
    res_s: [pd.Series] = []
    s: pd.Series = pd.Series()
    for sheet in excel_file.sheet_names:
        if (sheet != 'INFO') & ('ALMAK' not in sheet):
            c_name = sheet # обрезаем дату парсинга из названия вкладки
            print(f'=====> Analyses {sheet}:')
            s = BuildOneColumn(c_name, GetXData(excel_file, sheet))
            print(s)
            inp = input('Press ENTER to run next loop..')
            res_s.append(s)
        # print('Companies analysed: ', len(res_s))
        # print(res_s)
    df = pd.concat(res_s, axis=1)
    return pd.concat([result, df], axis=1)

def FindMatchedCar(car_name: str) -> str:
    M, _, _ = GetRData()
    sipp = 'nope'
    if car_name in M.index:
        if not pd.isna(M.loc[car_name, 'insp_sipp']):
            sipp = M.loc[car_name, 'insp_sipp'] + '_' + M.loc[car_name, 'park']
    return sipp

def GetTemplate_DF(T) -> pd.DataFrame:
    mi = GetMI(T)
    _, RN, RO = GetRData()
    F = lambda x: RN if x == 'new' else RO
    df = pd.DataFrame(index=mi)
    for s in T.sipp_names:
        for p in T.park:
            R = F(p)
            df.loc[s+'_'+p,'RAIDEN'] = R[R[R.columns[0]]=='Lim'].loc[:, s].to_numpy()

    print('RAIDEN RES')
    print(df)

    return df

def GetTemplate_S(name: str, T) -> pd.Series:
    mi = GetMI(T)
    return pd.Series(name = name, index=mi)

def GetRData():
    M = pd.read_excel(matches_root, index_col=0)
    RN = pd.read_excel(rates_root, "new", index_col=0, usecols=[0,1]+list(range(2, 18)), skiprows=lambda x: x not in [3]+list(range(6, 12))+list(range(17, 23)))
    RO = pd.read_excel(rates_root, "old", index_col=0, usecols=[0,1]+list(range(2, 18)), skiprows=lambda x: x not in [3]+list(range(6, 12))+list(range(17, 23)))
    return(M, RN, RO)

def GetXData(excel_file: pd.ExcelFile, sheet: str) -> pd.DataFrame:
    df = pd.read_excel(excel_file, sheet, index_col=0, skiprows=[0, 2, 3])
    # print('This DataX was got..')
    # print(sheet)
    # print(df.head(3))
    return df

def RenamedSIPPs(car_names: [str], columns: [str], matches: pd.DataFrame):
    # finds new Raiden SIPPs for company SIPPs and returns a dict for renaming
    # car_names - car names
    # columns - list of column names to be replaced
    # matches - DF got from matches table
    d = ['NOPE' if i != 'SIPP' else i for i in columns]
    for i in range(1, len(columns)):
        if car_names[i] in matches.index:
            m = matches.loc[car_names[i], 'insp_sipp']
            p = matches.loc[car_names[i], 'park']
            if not pd.isna(m): d[i] = m + ' ' + p
    return dict(zip(columns, d))

def GetMI(Trio) -> pd.MultiIndex:
    return pd.MultiIndex.from_product([[i+'_'+j for i in Trio.sipp_names for j in Trio.park], Trio.rate_names], names=['sipp', 'rate'])
