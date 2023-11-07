# REX RENT PARSER

from bs4 import BeautifulSoup
import requests
import pydantic
from dataclasses import dataclass
import datetime
from typing import List
import random

rexrent_api_url_LED = """https://www.rexrent.ru/reservation/?takePointLabel=%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3+%D0%90%D1%8D%D1%80%D0%BE%D0%BF%D0%BE%D1%80%D1%82+%D0%9F%D1%83%D0%BB%D0%BA%D0%BE%D0%B2%D0%BE&takePoint=LED%2C%2C&takePointInfo=%7B%22ID%22%3A%2237%22%2C%22name%22%3A%22%5Cu0410%5Cu044d%5Cu0440%5Cu043e%5Cu043f%5Cu043e%5Cu0440%5Cu0442+%5Cu041f%5Cu0443%5Cu043b%5Cu043a%5Cu043e%5Cu0432%5Cu043e%22%2C%22phone%22%3A%22%5C%22%2B7+921+315+16+31%5Cn%2B7+800+250+12+13+%28%5Cu0431%5Cu0435%5Cu0441%5Cu043f%5Cu043b%5Cu0430%5Cu0442%5Cu043d%5Cu044b%5Cu0439+%5Cu0432%5Cu044b%5Cu0437%5Cu043e%5Cu0432%29%5C%22%22%2C%22hours%22%3A%22%5Cu041f%5Cu041d-%5Cu0412%5Cu0421%3A+09%3A00-21%3A00%22%2C%22city%22%3A%22%5Cu0421%5Cu0430%5Cu043d%5Cu043a%5Cu0442-%5Cu041f%5Cu0435%5Cu0442%5Cu0435%5Cu0440%5Cu0431%5Cu0443%5Cu0440%5Cu0433%22%2C%22regione%22%3A%22%5Cu0421%5Cu0430%5Cu043d%5Cu043a%5Cu0442-%5Cu041f%5Cu0435%5Cu0442%5Cu0435%5Cu0440%5Cu0431%5Cu0443%5Cu0440%5Cu0433%22%2C%22address%22%3A%22%5Cu041f%5Cu0443%5Cu043b%5Cu043a%5Cu043e%5Cu0432%5Cu0441%5Cu043a%5Cu043e%5Cu0435+%5Cu0448.%2C+%5Cu0434.+41%2C+%5Cu043b%5Cu0438%5Cu0442.+3%5Cu0410%2C+2+%5Cu044d%5Cu0442%5Cu0430%5Cu0436%22%2C%22code%22%3A%22LED%22%2C%22is_airport%22%3A%221%22%2C%22latitude%22%3A%2259%2C7967%22%2C%22longitude%22%3A%2230%2C26943%22%2C%22zip%22%3A%22196210%22%2C%22location_name%22%3A%22PULKOVO+AIRPORT%22%2C%22address_one%22%3A%22International+Airport+Pulkovo%22%2C%22address_two%22%3A%22%22%2C%22city_en%22%3A%22St+Petersburg%22%2C%22region_en%22%3A%22St+Petersburg%22%2C%22phones%22%3A%5B%7B%22label%22%3A%22%5C%22%2B7+921+315+16+31%22%2C%22link%22%3A%22tel%3A%5C%2F%5C%2F%2B79213151631%22%7D%2C%7B%22label%22%3A%22%2B7+800+250+12+13+%28%5Cu0431%5Cu0435%5Cu0441%5Cu043f%5Cu043b%5Cu0430%5Cu0442%5Cu043d%5Cu044b%5Cu0439+%5Cu0432%5Cu044b%5Cu0437%5Cu043e%5Cu0432%29%5C%22%22%2C%22link%22%3A%22tel%3A%5C%2F%5C%2F%2B78002501213%22%7D%5D%2C%22time%22%3A%5B%22%5Cu041f%5Cu041d-%5Cu0412%5Cu0421%3A+09%3A00-21%3A00%22%5D%7D&takeDate={}&takeTime={}&returnPointLabel=%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3+%D0%90%D1%8D%D1%80%D0%BE%D0%BF%D0%BE%D1%80%D1%82+%D0%9F%D1%83%D0%BB%D0%BA%D0%BE%D0%B2%D0%BE&returnPoint=LED%2C%2C&returnPointInfo=%7B%22ID%22%3A%2237%22%2C%22name%22%3A%22%5Cu0410%5Cu044d%5Cu0440%5Cu043e%5Cu043f%5Cu043e%5Cu0440%5Cu0442+%5Cu041f%5Cu0443%5Cu043b%5Cu043a%5Cu043e%5Cu0432%5Cu043e%22%2C%22phone%22%3A%22%5C%22%2B7+921+315+16+31%5Cn%2B7+800+250+12+13+%28%5Cu0431%5Cu0435%5Cu0441%5Cu043f%5Cu043b%5Cu0430%5Cu0442%5Cu043d%5Cu044b%5Cu0439+%5Cu0432%5Cu044b%5Cu0437%5Cu043e%5Cu0432%29%5C%22%22%2C%22hours%22%3A%22%5Cu041f%5Cu041d-%5Cu0412%5Cu0421%3A+09%3A00-21%3A00%22%2C%22city%22%3A%22%5Cu0421%5Cu0430%5Cu043d%5Cu043a%5Cu0442-%5Cu041f%5Cu0435%5Cu0442%5Cu0435%5Cu0440%5Cu0431%5Cu0443%5Cu0440%5Cu0433%22%2C%22regione%22%3A%22%5Cu0421%5Cu0430%5Cu043d%5Cu043a%5Cu0442-%5Cu041f%5Cu0435%5Cu0442%5Cu0435%5Cu0440%5Cu0431%5Cu0443%5Cu0440%5Cu0433%22%2C%22address%22%3A%22%5Cu041f%5Cu0443%5Cu043b%5Cu043a%5Cu043e%5Cu0432%5Cu0441%5Cu043a%5Cu043e%5Cu0435+%5Cu0448.%2C+%5Cu0434.+41%2C+%5Cu043b%5Cu0438%5Cu0442.+3%5Cu0410%2C+2+%5Cu044d%5Cu0442%5Cu0430%5Cu0436%22%2C%22code%22%3A%22LED%22%2C%22is_airport%22%3A%221%22%2C%22latitude%22%3A%2259%2C7967%22%2C%22longitude%22%3A%2230%2C26943%22%2C%22zip%22%3A%22196210%22%2C%22location_name%22%3A%22PULKOVO+AIRPORT%22%2C%22address_one%22%3A%22International+Airport+Pulkovo%22%2C%22address_two%22%3A%22%22%2C%22city_en%22%3A%22St+Petersburg%22%2C%22region_en%22%3A%22St+Petersburg%22%2C%22phones%22%3A%5B%7B%22label%22%3A%22%5C%22%2B7+921+315+16+31%22%2C%22link%22%3A%22tel%3A%5C%2F%5C%2F%2B79213151631%22%7D%2C%7B%22label%22%3A%22%2B7+800+250+12+13+%28%5Cu0431%5Cu0435%5Cu0441%5Cu043f%5Cu043b%5Cu0430%5Cu0442%5Cu043d%5Cu044b%5Cu0439+%5Cu0432%5Cu044b%5Cu0437%5Cu043e%5Cu0432%29%5C%22%22%2C%22link%22%3A%22tel%3A%5C%2F%5C%2F%2B78002501213%22%7D%5D%2C%22time%22%3A%5B%22%5Cu041f%5Cu041d-%5Cu0412%5Cu0421%3A+09%3A00-21%3A00%22%5D%7D&returnDate={}&returnTime={}&partners=&partner_code=&autoId="""

class spData (pydantic.BaseModel):
    d: dict

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
    
resultList: List[CarForRent] = []

def formatDate(date: datetime.date) -> str:
    return date.strftime("%d.%m.%Y")

def formatTime() -> str:
    return (f"{random.randint(10, 20)}%3A00")

def existedSIPP(sipp: str) -> int:
    global resultList
    for i in range(0, len(resultList)):
        if sipp == resultList[i].sipp:
            return i
    return -1

def recordRate(i: int, days: int, rate: float):
    global resultList
    if days == 1:
        resultList[i].rate1 = rate
        return
    if days == 3:
        resultList[i].rate3 = rate
        return
    if days == 7:
        resultList[i].rate7 = rate
        return
    if days == 14:
        resultList[i].rate14 = rate
        return
    if days == 21:
        resultList[i].rate21 = rate
        return
    if days == 30:
        resultList[i].rate30 = rate
        return

def getOneColomnRates(pick_up: datetime.date, days: int, url: str, session):
    global resultList
    __delta = datetime.timedelta(days)
    drop_off = pick_up + __delta
    pick_up_str = formatDate(pick_up)
    drop_off_str = formatDate(drop_off)
    t = formatTime()
    __url_final = url.format(pick_up_str, t, drop_off_str, t)
    soup = BeautifulSoup(session.get(url=__url_final).text, 'lxml')
    for el in soup.find_all('div', attrs={'class':'rental_item item'}):
        i = existedSIPP(el.get('data-group'))
        if i == -1:
            car = CarForRent(
                            el.get('data-group'),
                            el.get('data-car-name'),
                            )
            car.depo = float(el.find('span', attrs={'class':'other-feature-item'}).contents[0][8:-1])
            resultList.append(car)
            i = existedSIPP(el.get('data-group'))
        recordRate(i, days, round(float(el.get('data-car-price'))/days, 2))

with requests.Session() as s:
    rates = [1, 3, 7, 14, 21, 30]
    pick_up = datetime.datetime.today() + datetime.timedelta(3)
    for days in rates:
        getOneColomnRates(pick_up, days, rexrent_api_url_LED, s)
    s.close()

    print(f'{len(resultList)} cars were found..')
    print()
    for c in resultList:
        print(c.sipp, "<", c.name, ">", c.depo, c.rate1, c.rate3, c.rate7, c.rate14, c.rate21, c.rate30)