from config import ALMAK_TARIFFS_URL_SPB as url
from config import ALMAK_KATALOG_PREFIX as katalog_prefix
from bs4 import BeautifulSoup
import datetime
import requests
from typing import List
from objects import CFR

import asyncio
import aiohttp

def getCarType(i: int) -> str:
    types = ['Promo', 'Standart', 'Comfort', 'SUV', 'Van', 'Business', 'Commercial']
    j = i%7
    return types[j]

async def getXtraInfo(res_list: List[CFR], session: aiohttp.ClientSession) -> List[CFR]:
    for c in res_list:
        async with session.get(katalog_prefix + c.url) as __response:
            soup = BeautifulSoup(await __response.text(), 'lxml')
            UL = soup.find('ul', {'class': 'hinfo'})
            LI = UL('li')
            Xtras = []
            for l in LI:
                if len(l.contents) > 1:
                    Xtras.append(l.contents[1])
                else:
                    Xtras.append('N/A')
            c.gear_box = Xtras[0]
            c.engine = Xtras[1]
            c.MY = Xtras[2]
            depo = Xtras[5].replace(" ", "")[:-4]
            depo = depo.replace('\xa0', '')
            try:
                c.depo = float(depo)
            except Exception as E:
                print(E)
            c.driving_experience = Xtras[6]
            c.min_age = Xtras[7]
    return res_list

async def getOneColumnRates_almak(res_list: List[CFR], pick_up: datetime.date, days: int, session: aiohttp.ClientSession, *args, **kwargs) -> List[CFR]:
    async with session.get(url=url) as __response:
        print(f"{url[:60]}.. Status code: ", __response.status, "..")
        if __response.status >= 400:
            return None
        soup = BeautifulSoup(await __response.text(), 'lxml')
        TABLES = soup('table')
        for i in range(21):
            rows = TABLES[i]('tr')
            for tr in rows:
                if len(tr('th')) == 0:
                    car = CFR("", "")
                    car.different_millages = True
                    car.company = "ALMAK PROKAT"
                    if i < 7:
                        car.millage = 200
                    elif i < 14:
                        car.millage = 300
                    else:
                        car.millage = 500
                    car.url = tr.td.a.get('href')
                    car.carType = getCarType(i)
                    car.name = tr.td.a.string
                    td = tr('td')
                    car.setRate(1, float(td[1].string[:-5]))
                    car.setRate(3, float(td[2].string[:-5]))
                    car.setRate(7, float(td[3].string[:-5]))
                    car.setRate(14, float(td[3].string[:-5]))
                    car.setRate(21, float(td[4].string[:-5]))
                    car.setRate(30, float(td[4].string[:-5]))
                    res_list.append(car)
        xtra = kwargs.get('xtra')
        if xtra == None: xtra=False
        if xtra:
            res_list = await getXtraInfo(res_list, session)
        return res_list