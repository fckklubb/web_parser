from config import STORLET_URL_SPB as url
from helpers import findCarByName, formatDate, formatTime
from bs4 import BeautifulSoup
import datetime
import requests
from typing import List
from objects import CFR

def getOneColumnRates(res_list: List[CFR], pick_up: datetime.date, days: int, session: requests.Session, *args, **kwargs) -> List[CFR]:
    drop_off = pick_up + datetime.timedelta(days)
    time = formatTime()
    __url = url.format(formatDate(pick_up, 1), time, formatDate(drop_off, 1), time)
    __response = session.get(url=__url)
    print(f"{__url[:60]}.. Status code: ", __response.status_code, "..")
    if __response.status_code >= 400:
        return None
    soup = BeautifulSoup(__response.text, 'lxml')
    car_divs = soup('div', attrs={'class':'row car_item'})
    for car_div in car_divs:
        car_name = car_div.find('a', attrs={'data-gtm-event':'autos_auto_title'}).p.string
        i = findCarByName(car_name, res_list)
        if i == -1:
            car = CFR(name=car_name)
            car.company = "STORLET CARS"
            car.sipp = list(car_div.attrs.keys())[1][12:]
            car.depo = float(car_div.find('div', attrs={'class':'bonds'}).div.next_sibling)
            car.setRate(days, float(car_div.find('div', attrs={'class':'col-md-8 prices'}).h2.span.next_sibling))
            res_list.append(car)
        res_list[i].setRate(days, float(car_div.find('div', attrs={'class':'col-md-8 prices'}).h2.span.next_sibling))
    return res_list