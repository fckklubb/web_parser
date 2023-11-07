from config import REXRENT_API_URL_LED as url
from helpers import findCarBySIPP, formatDate, formatTime
from bs4 import BeautifulSoup
import datetime
import requests
from typing import List
from objects import CFR

def getOneColumnRates(res_list: List[CFR], pick_up: datetime.date, days: int, session: requests.Session, *args, **kwargs) -> List[CFR]:
    __delta = datetime.timedelta(days)
    drop_off = pick_up + __delta
    t = formatTime()
    __url = url.format(formatDate(pick_up, 3), t, formatDate(drop_off, 3), t)
    __response = session.get(url=__url)
    print(f"{__url[:60]}.. Status code: ", __response.status_code, "..")
    if __response.status_code >= 400:
        return None
    soup = BeautifulSoup(__response.text, 'lxml')
    for el in soup.find_all('div', attrs={'class':'rental_item item'}):
        i = findCarBySIPP(el.get('data-group'), res_list)
        if i == -1:
            car = CFR(
                            el.get('data-group'),
                            el.get('data-car-name'),
                            )
            car.company = "REX RENT"
            car.depo = float(el.find('span', attrs={'class':'other-feature-item'}).contents[0][8:-1])
            res_list.append(car)
            i = len(res_list)-1
        res_list[i].setRate(days, round(float(el.get('data-car-price'))/days, 2))
    return res_list