from config import RENTMOTORS_API_URL as url
from config import RENTMOTORS_STATONS as stations
from helpers import findCarBySIPP, formatDate, formatTime
from bs4 import BeautifulSoup
import json
import datetime
import requests
from typing import List
from objects import CFR
import asyncio
import aiohttp

async def getOneColumnRates(res_list: List[CFR], pick_up: datetime.date, days: int, session: aiohttp.ClientSession, *args, **kwargs) -> List[CFR]:
    __delta = datetime.timedelta(days)
    drop_off = pick_up + __delta
    time = formatTime()
    location = kwargs.get('location')
    __url = url.format(location, location, formatDate(pick_up, 2), time, formatDate(drop_off, 2), time)
    async with session.get(url=__url) as __response:
        print(f"{__url[:60]}.. Status code: ", __response.status, "..")
        if __response.status >= 400:
            return None
        soup = BeautifulSoup(await __response.text(), 'lxml')
        data = json.loads(soup.get_text())
        for el in data:
            i = findCarBySIPP(el["car_info"]["code"], res_list)
            if i == -1:
                car = CFR(
                                el["car_info"]["code"],
                                el["car_info"]["car_name"],
                                float(el["car_info"]["deposit"]),
                                )
                car.company = "RENT MOTORS"
                res_list.append(car)
                i = len(res_list)-1
            res_list[i].setRate(days, round(float(el["day_price"])/float(el["days"]), 2))
        return res_list