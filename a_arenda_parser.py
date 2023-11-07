from config import RENTCARS_API_URL_SPB as url
from helpers import findCarByName, formatDate
from bs4 import BeautifulSoup
import datetime
import requests
from typing import List
from objects import CFR

def getOneColumnRates(res_list: List[CFR], pick_up: datetime.date, days: int, session: requests.Session, *args, **kwargs) -> List[CFR]:
    __delta = datetime.timedelta(days)
    drop_off = pick_up + __delta
    __url = url.format(formatDate(pick_up, 2), formatDate(drop_off, 2))
    __response = session.get(url=__url)
    print(f"{__url[:60]}.. Status code: ", __response.status_code, "..")
    if __response.status_code >= 400:
        return None
    soup = BeautifulSoup(__response.text, 'lxml')
    blocks = soup.find_all('div', attrs={'class':'row'})
    for x in range(1, len(blocks), 2):
        item = blocks[x].contents
        i = findCarByName(item[1].a.string, res_list)
        if i == -1:
            car = CFR(
                            item[3].string,
                            item[1].a.string,
                            )
            car.company = "A-ARENDA (ARENDA AVTO)"
            car.depo = float(item[9].string.replace(" ", "")[:-5])
            res_list.append(car)
            i = len(res_list) - 1
        res_list[i].setRate(days, round(float(item[5].string.replace(" ", "")[:-5])/days, 2))
    return res_list