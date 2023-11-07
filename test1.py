from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import json
import requests

# service = Service(r"r:\PROJECTS\PYTHON\WEB_PARSER\chromedrv")
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('--remote-debugging-port=9222')
# options.add_argument('--enable-javascript')
# options.add_argument('--user-agent=\'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0\'')
# options.add_argument('--no-sandbox')
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--allow-insecure-localhost')
# options.add_argument('--ignore-certificate-errors')

# browser = webdriver.Chrome(service=service, options=options)
# browser.get('https://rentmotors.ru/api/cars?start_station=6&end_station=6&start_date=2023-07-21+10:00&end_date=2023-07-30+10:00&age=1&sourceid=0')
# requiredHtml = browser.page_source
# time.sleep(2)

# soup = BeautifulSoup(requiredHtml, 'html5lib')
# data = soup.find('pre').text
# print(data[1:-1])

# list_we_got = json.loads(data)

# print(list_we_got[0])

# dict_we_got = json.loads(str(list_we_got[0]))

# print(type(dict_we_got))

# print(len(dict_we_got))
# print(dict_we_got["car_info"])
# browser.quit()
# browser.close()

# url = "https://spb.europcar.ru/order/step2/"
# url = "http://spb.inspirerent.ru/order/step2/"
url = "http://spb.inspirerent.ru/order/step2/?rate_id=1525515&point_from=%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9+%28%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B5+%D1%88%D0%BE%D1%81%D1%81%D0%B5%2C+13%2F8+%D0%94+%29&point_from_id=10781&point_to=%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9+%28%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B5+%D1%88%D0%BE%D1%81%D1%81%D0%B5%2C+13%2F8+%D0%94+%29&point_to_id=10781&date_from=21.07.2023&date_to=23.07.2023&time_from=9%3A00&time_to=9%3A00&dif_days=0&express_hours=0&extra_hours=0&race_number_from=&race_number_to="
# url = "https://spb.europcar.ru/order/step2/?rate_id=1540540&point_from=%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9+%28%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B5+%D1%88%D0%BE%D1%81%D1%81%D0%B5%2C+13%2F8+%D0%94+%29&point_from_id=10781&point_to=%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9+%28%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B5+%D1%88%D0%BE%D1%81%D1%81%D0%B5%2C+13%2F8+%D0%94+%29&point_to_id=10781&date_from=21.07.2023&date_to=25.07.2023&time_from=%0D%0A++++++++++++++++++++++++9%3A00&time_to=%0D%0A++++++++++++++++++++++++9%3A00&dif_days=0&express_hours=0&extra_hours=0&race_number_from=&race_number_to="
myobj = {'rate_id':'1540540',
         'point_from':'Центральный+(Московское+шоссе,+13/8+Д+)',
         'point_from_id':'10781',
         'point_to':'Центральный+(Московское+шоссе,+13/8+Д+)',
         'point_to_id':'10781',
         'date_from':'21.07.2023',
         'date_to':'23.07.2023',
         'time_from':'9:00',
         'time_to':'9:00',
         'dif_days':'0',
         'express_hours':'0',
         'extra_hours':'0',
         'race_number_from':'',
         'race_number_to':''
         }

# x = requests.post(url, json = myobj)
x = requests.get(url)
soup = BeautifulSoup(x.text, 'lxml')
for el in soup.find_all('div', attrs={'class':'slider_car'}):
    print("The car: ", el.get('data-car_name'), "dayrate: ", el.get('data-price'), "discount: ", el.get('data-discount'))
    dayrate = float(el.get('data-price'))
    if el.get('data-discount') != "":
        dayrate = float(el.get('data-price'))*(1 - 0.01 * float(el.get('data-discount')[2:]))
    print(f"{el.get('data-car_name')} ==> {dayrate} RUBS per day.")
x.close()