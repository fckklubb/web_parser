# ALMAK PROKAT PARSER (https://avto-prokat.spb.ru/)

from bs4 import BeautifulSoup
import requests
import pydantic
from dataclasses import dataclass
import datetime
from typing import List
import random

almak_prokat_tariffs_url_spb = "https://avto-prokat.spb.ru/tarify/"
katalog_prefix = "https://avto-prokat.spb.ru"

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

class CFR(CarForRent):
    carType: str = ""
    millage: int = 0
    url: str = ""
    MY: str = ""
    driving_experience: str = ""
    min_age: str = ""
    gear_box: str = ""
    engine: str = ""

resultList: List[CFR] = []

def existedName(name: str) -> int:
    global resultList
    for i in range(0, len(resultList)):
        if name == resultList[i].name:
            return i
    return -1

def getCarType(i: int) -> str:
    types = ['Promo', 'Standart', 'Comfort', 'SUV', 'Van', 'Business', 'Commercial']
    j = i%7
    return types[j]

def getOneColomnRates(url: str, session):
    global resultList
    soup = BeautifulSoup(session.get(url=url).text, 'lxml')
    TABLES = soup('table')
    for i in range(21):
        rows = TABLES[i]('tr')
        for tr in rows:
            if len(tr('th')) == 0:
                car = CFR("", "")
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
                resultList.append(car)

def getXtraInfo(session):
    global resultList
    for c in resultList:
        soup = BeautifulSoup(session.get(katalog_prefix + c.url).text, 'lxml')
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

with requests.Session() as s:
    getOneColomnRates(almak_prokat_tariffs_url_spb, s)
    getXtraInfo(s)
    s.close()

    print(f'{len(resultList)} cars were found..')
    for c in resultList:
        print(c.sipp, c.millage, c.carType, "<", c.name, c.MY, c.min_age, c.driving_experience, ">", c.depo, c.rate1, c.rate3, c.rate7, c.rate14, c.rate21, c.rate30)