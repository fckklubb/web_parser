# STORLET CARS PARSER (https://storletcar.com/)
# &start_date=03-08-2023&start_time=12%3A00&end_date=09-08-2023&end_time=12%3A00
# pick_up_date, pick_up_time, drop_off_date, drop_off_time

from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import datetime
from typing import List
import random

#SPB
# URL_STORLET = "https://storletcar.com/ru/spb/cars?utf8=%E2%9C%93&region=5639be176672693344000000&delivery=5639be1b6672693344fa0000&return=5639be1b6672693344fa0000&start_date={}&start_time={}&end_date={}&end_time={}"
#MSK
URL_STORLET = "https://storletcar.com/ru/msk/cars?utf8=%E2%9C%93&region=5639be196672693344450000&delivery=566ff35b6672697143960000&return=566ff35b6672697143960000&start_date={}&start_time={}&end_date={}&end_time={}"

@dataclass
class CarForRent:
    sipp: str = ""
    name: str = ""
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
rates = [1, 3, 7, 14, 21, 30]

def existedName(name: str) -> int:
    global resultList
    for i in range(0, len(resultList)):
        if name == resultList[i].name:
            return i
    return -1

def getOneColumnRate(pick_up: datetime.date, days: int, session):
    global resultList
    drop_off_txt = formatDate(pick_up + datetime.timedelta(days))
    pick_up_txt = formatDate(pick_up)
    time = formatTime()
    url = URL_STORLET.format(pick_up_txt, time, drop_off_txt, time)
    soup = BeautifulSoup(session.get(url=url).text, 'lxml')
    car_divs = soup('div', attrs={'class':'row car_item'})
    for car_div in car_divs:
        car_name = car_div.find('a', attrs={'data-gtm-event':'autos_auto_title'}).p.string
        i = existedName(car_name)
        if i == -1:
            car = CFR(name=car_name)
            car.sipp = list(car_div.attrs.keys())[1][12:]
            car.depo = float(car_div.find('div', attrs={'class':'bonds'}).div.next_sibling)
            car.setRate(days, float(car_div.find('div', attrs={'class':'col-md-8 prices'}).h2.span.next_sibling))
            resultList.append(car)
        resultList[i].setRate(days, float(car_div.find('div', attrs={'class':'col-md-8 prices'}).h2.span.next_sibling))

def formatDate(date: datetime.date) -> str:
    return date.strftime("%d-%m-%Y")

def formatTime() -> str:
    return (f"{random.randint(10, 20)}%3A00")

if __name__ == '__main__':
    with requests.Session() as s:
        pick_up = datetime.datetime.today() + datetime.timedelta(5)
        time = formatTime()
        for rate in rates:
            getOneColumnRate(pick_up, rate, s)
        s.close()
    print("We find cars: ", len(resultList))
    for car in resultList:
        print(car.sipp, car.name, car.depo, car.rate1, car.rate3, car.rate7, car.rate14, car.rate21, car.rate30)