# A-ARENDA PARSER (www.rentcars.ru)

from bs4 import BeautifulSoup
import requests
import pydantic
from dataclasses import dataclass
import datetime
from typing import List
import random

rentcars_api_url_msk = "https://www.rentcars.ru/index.php?mact=aa_mod_tariff,cntnt01,cli_rs_tariff_list,0&cntnt01dtb={}&cntnt01dte={}&cntnt01class_ids=&cntnt01returnid=8&showtemplate=false"
rentcars_api_url_spb = "https://www.rentcars.ru/index.php?mact=aa_mod_tariff,cntnt01,cli_rs_tariff_list,0&cntnt01dtb={}&cntnt01dte={}&cntnt01class_ids=&cntnt01returnid=38&showtemplate=false"

@dataclass
class CarForRent:
    sipp: str
    name: str
    depo: float = 0
    rate1: float = 0
    rate3: float = 0
    rate7: float = 0
    rate14: float = 0
    rate21: float = 0
    rate30: float = 0

    def setRate(self, days: int, rate: float):
        if days == 1:
            self.rate1 = rate
            return
        if days == 3:
            self.rate3 = rate
            return
        if days == 7:
            self.rate7 = rate
            return
        if days == 14:
            self.rate14 = rate
            return
        if days == 21:
            self.rate21 = rate
            return
        if days == 30:
            self.rate30 = rate
            return
    
resultList: List[CarForRent] = []

def formatDate(date: datetime.date) -> str:
    return date.strftime("%Y-%m-%d")

def existedName(name: str) -> int:
    global resultList
    for i in range(0, len(resultList)):
        if name == resultList[i].name:
            return i
    return -1

def getOneColomnRates(pick_up: datetime.date, days: int, url: str, session):
    global resultList
    __delta = datetime.timedelta(days)
    drop_off = pick_up + __delta
    pick_up_str = formatDate(pick_up)
    drop_off_str = formatDate(drop_off)
    __url_final = url.format(pick_up_str, drop_off_str)
    soup = BeautifulSoup(session.get(url=__url_final).text, 'lxml')
    blocks = soup.find_all('div', attrs={'class':'row'})
    for x in range(1, len(blocks), 2):
        item = blocks[x].contents
        i = existedName(item[1].a.string)
        if i == -1:
            car = CarForRent(
                            item[3].string,
                            item[1].a.string,
                            )
            car.depo = float(item[9].string.replace(" ", "")[:-5])
            resultList.append(car)
            i = len(resultList) - 1
        resultList[i].setRate(days, round(float(item[5].string.replace(" ", "")[:-5])/days, 2))

with requests.Session() as s:
    rates = [1, 3, 7, 14, 21, 30]
    pick_up = datetime.datetime.today() + datetime.timedelta(3)
    for days in rates:
        getOneColomnRates(pick_up, days, rentcars_api_url_msk, s)
    s.close()

    print(f'{len(resultList)} cars were found..')
    for c in resultList:
        print(c.sipp, "<", c.name, ">", c.depo, c.rate1, c.rate3, c.rate7, c.rate14, c.rate21, c.rate30)