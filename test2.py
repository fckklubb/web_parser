# RENT MOTORS PARSING
from bs4 import BeautifulSoup
import json
import requests
from dataclasses import dataclass
import datetime
from typing import List
import random
import pandas as pd

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

rentmotors_api_url = "https://rentmotors.ru/api/cars?start_station={}&end_station={}&start_date={}+{}&end_date={}+{}&age=1&sourceid=0"
parsedList: List[CarForRent] = []
stations = {"MSK_CO":2, "SVO":3, "LED":16, "SPB_CO":10}

def existedSIPP(sipp: str) -> int:
    for i in range(0, len(parsedList)):
        if sipp == parsedList[i].sipp:
            return i
    return -1

def formatDate(date: datetime.date) -> str:
    return date.strftime("%Y-%m-%d")

def formatTime() -> str:
    return (f"{random.randint(10, 20)}:00")

def getOneColomnRates(pick_up: datetime.date, days: int, location: int, session):
    __delta = datetime.timedelta(days)
    drop_off = pick_up + __delta
    pick_up_str = formatDate(pick_up)
    drop_off_str = formatDate(drop_off)
    t = formatTime()
    __url = rentmotors_api_url.format(location, location, pick_up_str, t, drop_off_str, t)
    soup = BeautifulSoup(session.get(url=__url).text, 'lxml')
    data = json.loads(soup.get_text())
    for el in data:
        i = existedSIPP(el["car_info"]["code"])
        if i == -1:
            car = CarForRent(
                            el["car_info"]["code"],
                            el["car_info"]["car_name"],
                            float(el["car_info"]["deposit"]),
                            )
            parsedList.append(car)
            i = len(parsedList)-1
        parsedList[i].setRate(days, round(float(el["day_price"])/float(el["days"]), 2))

def carTable(list: CarForRent) -> pd.DataFrame:
    index = ['SIPP', 'Name', 'Depo', 'R1', 'R3', 'R7', 'R14', 'R21', 'R30']
    res_list: dict = {}
    for car in list:
        res_list[car.name] = pd.Series([car.sipp, car.name, car.depo, car.rate1, car.rate3, car.rate7, car.rate14, car.rate21, car.rate30], index=index)
    return pd.DataFrame(res_list)

if __name__ == '__main__':
    print("Let's get started..")
    strat_point = datetime.datetime.today()
    with requests.Session() as s:
        rates = [1, 3, 7, 14, 21, 30]
        pick_up = datetime.datetime.today() + datetime.timedelta(4)
        for days in rates:
            getOneColomnRates(pick_up, days, stations['SPB_CO'], s)
        s.close()

    print(f'{len(parsedList)} cars were found..')
    df = carTable(parsedList)
    df.to_excel("rent_motors.xlsx", sheet_name=f'RENTMOTORS-{datetime.datetime.today().strftime("%d-%m-%Y")}')
    print("File 'rent_motors.xlsx' created..")
    print(f"Total processing time: {(datetime.datetime.today() - strat_point).seconds}sec..")