import asyncio
import aiohttp
import datetime
from typing import List
import random
import requests
from objects import CFR
from config import RATES

def formatDate(date: datetime.date, type: int) -> str:
    if type == 1:
        return date.strftime("%d-%m-%Y")
    elif type == 2:
        return date.strftime("%Y-%m-%d")
    elif type == 3:
        return date.strftime("%d.%m.%Y")
    return ""

def formatTime() -> str:
    return (f"{random.randint(10, 20)}%3A00")

def findCarBySIPP(sipp: str, data: List[CFR]) -> int:
    for d in data:
        if sipp == d.sipp:
            return data.index(d)
    return -1

def findCarByName(name: str, data: List[CFR]) -> int:
    for d in data:
        if name == d.name:
            return data.index(d)
    return -1

async def getAllRates(pick_up: datetime.date, session: aiohttp.ClientSession, f, *args, **kwargs) -> List[CFR]:
    res_list: List[CFR] = []
    
    location = kwargs.get('location')
    if location == None: location = ""
    
    loop = kwargs.get('loop')
    if loop == None: loop = True
    
    xtra = kwargs.get('xtra')
    if xtra == None: xtra = False
    
    print(f'KWARGS from {f.__name__}: location={location}, loop={loop}, xtra={xtra}')

    if loop:
        for rate in RATES:
            res_list = await f(res_list, pick_up, rate, session, location=location)
        print("Found:", len(res_list), "cars..")
    else:
        res_list = await f(res_list, pick_up, 0, session, xtra=xtra)
        print("Found:", len(res_list)//3, "cars..")
    return res_list