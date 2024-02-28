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
                if result[[(sipp, f'{x}') for x in Trio.rate_names]].isna().any():
                    result[[(sipp, f'{x}') for x in Trio.rate_names]] = data[x].to_numpy()
                    result[(sipp, 'car_name')] = x
                else:
                    rr = result[[(sipp, f'{x}') for x in Trio.rate_names]].reset_index(drop=True) > data[x].reset_index(drop=True)
                    if rr.any(): # OR ALL ?!?!
                        result[[(sipp, f'{x}') for x in Trio.rate_names]] = data[x].to_numpy()
                        result[(sipp, 'car_name')] = x
    return result

def GatherAllColumns(excel_file: pd.ExcelFile):
    result = GetTemplate_DF(Trio)
    res_s: [pd.Series] = []
    s: pd.Series = pd.Series()
    for sheet in excel_file.sheet_names:
        # if (sheet != 'INFO') & ('ALMAK' not in sheet):
        if sheet != 'INFO':
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
    else:
        pass
        # тут нужно написать функцию для добавления
        # car_name в matches
        # AddCarToList(car_name)
    return sipp

def GetTemplate_DF(T) -> pd.DataFrame:
    mi = GetMI(T)
    _, RN, RO = GetRData()
    F1 = lambda x: RN if x == 'new' else RO
    fleet_new, fleet_old = GetRFleet()
    F2 = lambda x: fleet_new if x == 'new' else fleet_old
    df = pd.DataFrame(index=mi)
    for s in T.sipp_names:
        for p in T.park:
            R = F1(p)
            df.loc[[(s+'_'+p, f'{x}') for x in T.rate_names],'RAIDEN'] = R[R[R.columns[0]]=='Lim'].loc[:, s].to_numpy()
            F = F2(p)
            df.loc[(s+'_'+p, 'car_name'), 'RAIDEN'] = F.at[0, s]

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

def GetRFleet():
    fleet_new_ = pd.read_excel(rates_root, "new", header=None, usecols=list(range(2, 18)), skiprows= lambda x: x not in [0])
    sipps_new_ = pd.read_excel(rates_root, "new", header=None, usecols=list(range(2, 18)), skiprows= lambda x: x not in [3])
    fleet_old_ = pd.read_excel(rates_root, "old", header=None, usecols=list(range(2, 18)), skiprows= lambda x: x not in [0])
    sipps_old_ = pd.read_excel(rates_root, "old", header=None, usecols=list(range(2, 18)), skiprows= lambda x: x not in [3])
    
    d = dict(zip(fleet_new_.columns.to_numpy().tolist(), sipps_new_.loc[0].to_numpy().tolist()))
    fleet_new_ = fleet_new_.rename(columns=d)

    d = dict(zip(fleet_old_.columns.to_numpy().tolist(), sipps_old_.loc[0].to_numpy().tolist()))
    fleet_old_ = fleet_old_.rename(columns=d)
    
    return (fleet_new_, fleet_old_)

def GetXData(excel_file: pd.ExcelFile, sheet: str) -> pd.DataFrame:
    df = pd.read_excel(excel_file, sheet, index_col=0, skiprows=[0, 2, 3], nrows=6)
    # nrows = 6 - for Almak OR diff mileage companies первые строки 6 штук - для пробена 200 в сутки :-)
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
    c = ['car_name']
    c.extend(Trio.rate_names)
    return pd.MultiIndex.from_product([[i+'_'+j for i in Trio.sipp_names for j in Trio.park], c], names=['sipp', 'rate'])

def AddCarToList():
    pass