from bs4 import BeautifulSoup
import datetime
import requests
from typing import List
from objects import CFR
from helpers import formatDate, findCarByName, findCarBySIPP

import asyncio
import aiohttp
import json
import brotli
import random

url = "https://www.economybookings.com/gapi?method=carlist"

def getReqInEBformat(put: datetime.date, dot: datetime.date, loc: str):
    REQ_1 = "{ bcrm (language: \"ru\") {\n      carlist(pickup_time: \""
    REQ_2 = "\" dropoff_time: \""
    REQ_3 = "\" driver_age: \"35\" coupon: \"\" pickup_location_id: \""
    REQ_4 = "\" dropoff_location_id: \""
    REQ_5 = "\" countryOfResidence: 183 customerCurrency: \"RUB\" cinfo: \"34a8d05b7fc62ff76d05ef7ccfc2da57|881163639.1709820149|0\" corFromUrl: 1 isSignedInCustomer: false isQuote: false){\n          cars {\n            \n  car {\n    additionalCompanyClass\n    airbag\n    airco\n    bigSuitcases\n    carTypeForWeb\n    classCode\n    companyClass\n    doors\n    fuel\n    group\n    id\n    imageUrl\n    name\n    seats\n    smallSuitcases\n    transmission\n  }\n\n            \n  station {\n    \n  address\n  company\n  email1\n  email2\n  id\n  instructions\n  latitude\n  location\n  locationAltName\n  locationId\n  longitude\n  openingHours\n  phone1\n  phone2\n  wherePickUp\n  locationCode\n  isNoMap\n\n  }\n\n            \n  freeExtras {\n    id\n    code\n    currency\n    customerMaxPrice\n    customerPrice\n    customerRate\n    extraImageType\n    isFreeByRefund\n    isIgnoredForWeb\n    isUnchecked\n    isWithoutPrice\n    localMaxPrice\n    localPrice\n    maxPrice\n    name\n    price\n    tax\n    usdPrice\n  }\n\n            \n  usdPrice {\n    aFExtraPrice\n    aFPrice\n    basePrice\n    currency\n    netPrice\n    taxAmount\n    total\n    maxDeposit\n    maxExcess\n    totalByCma\n  }\n\n            \n  customerPrice {\n    couponDiscount\n    couponDiscountType\n    couponDiscountPercent\n    basePrice\n    currency\n    total\n    totalByCma\n    maxDeposit\n    maxExcess\n  }\n\n            \n  price {\n    aFExtraPrice\n    aFPrice\n    basePrice\n    carRentalPriceInTakenCurr\n    commision\n    currency\n    deposit\n    netPrice\n    remainder\n    supplierDeposit\n    taxAmount\n    total\n    totalByCma\n  }\n\n            \n  supplier {\n    childSupplier\n    aggregatorMappingId\n    parentSupplier {\n      id\n      name\n      rating\n      isFromAggregator\n      aggregatorMappingId\n      includedFeatures {\n          featuresInfo\n      }\n    }\n    depositType\n    id\n    isFromAggregator\n    logo\n    name\n    rating\n    stationId\n    isBundle\n    reviewCount\n  }\n\n            \n  seasonExtras {\n    id\n    name\n  }\n\n            \n  carPromoDetailed {\n    promo\n    pictureUrl\n    documentUrl\n  }\n\n            \n  carPromoOptions {\n    category\n    code\n    localizedName\n    priority\n    labelHtmlColor\n    textHtmlColor\n  }\n\n            \n  carCount\n  chauffeurService\n  fuelPolicy\n  isNonRefundable\n  isOnRequest\n  isOnlineCheckinAvailable\n  millageLimit\n  millageLimitEn\n  supplierAccountNumber\n  carPromo\n  isFreeCancellation\n  freeCancellationDate\n  depInfo\n  carPopularity\n  pickupLocationId\n  dropoffLocationId\n  requestId\n\n          }\n          \n  suppliers {\n    aggregatorMappingId\n    carDiscount\n    companyGroupId\n    couponDiscount\n    depositType\n    groupRating\n    id\n    includedFeatures {\n        featuresInfo\n    }\n    isFromAggregator\n    logo\n    name\n    address\n    phone1\n    phone2\n    parentId\n    rating\n    reviewCount\n    reviews {\n      questionid\n      avgrating\n      question\n    }\n    hasAward\n  }\n\n          \n  stations {\n    \n  address\n  company\n  email1\n  email2\n  id\n  instructions\n  latitude\n  location\n  locationAltName\n  locationId\n  longitude\n  openingHours\n  phone1\n  phone2\n  wherePickUp\n  locationCode\n  isNoMap\n\n  }\n\n          \n  pickup {\n    id\n    locationType\n    location\n    locationAltName\n    country\n    countryAltName\n    city\n    cityAltName\n    locationCode\n    countryCode\n    date\n    time\n    locationUtc\n  }\n\n          \n  dropoff {\n    id\n    locationType\n    location\n    locationAltName\n    country\n    countryAltName\n    city\n    cityAltName\n    locationCode\n    countryCode\n    date\n    time\n  }\n\n          \n  defaultSortForCars\n  isSubscribedByDefault\n  clientRefenceId\n  fingerPrintId\n  gaClientId\n  integrationType\n  requestId\n  duration\n  error\n  isStationsWithoutMap\n\n        }\n    }}"
    rand_t__ = random.randint(10, 20)
    put__ = formatDate(put, 4) + rand_t__
    dot__ = formatDate(dot, 4) + rand_t__
    if isinstance(loc, str): return "loc_error" 
    else: return {"query": REQ_1 + put__ + REQ_2 + dot__ + REQ_3 + loc + REQ_4 + loc + REQ_5}

def work_with_response(response):
    decoded_txt = '{/"error/": /"Economy Booking server returned a wrong data../"}'
    if response.ok & ('br' in response.headers.get('Content-Encoding')):
        try:
            decoded_txt = brotli.decompress(response.content)
        except Exception as e:
            print('Error occured while decoding..', e)
            decoded_txt = response.content
    
    try:
        decoded_txt = json.loads(decoded_txt)
    except Exception as e:
        return {'error': 'Cant read an aswer from EB server as JSON..'}
    return {'sataus': 'OK', 'response': decoded_txt}

def verifyResponse(response):
    if 'error' in response:
        return False
    elif response.get('status') == 'OK':
        return True
    else:
        return False

def setHeaders():
    return {
            "Host": "www.economybookings.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept": "application/json",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "X-GApi-Method": "bcrm-carlist"
            }

def getData(res_list: List[CFR], answ, days: int) -> List[CFR]:
    for c in answ:
        i = findCarByName(c.get('car').get('name'), res_list)
        if i == -1:
            car = CFR() #тут нужно зансти данные типа депо и кода сипп и проч., смотреть структуру ответа json через инструменты разработчика
            car.company = "ECONOMY BOOKING: " + c.get('supplier').get('name')
            res_list.append(car)
            i = len(res_list)-1
        res_list[i].setRate(days, float(c.get('customerPrice').get('total'), 2)/days)

    return res_list

async def getOneColumnRates(res_list: List[CFR], pick_up: datetime.date, days: int, session: aiohttp.ClientSession, *args, **kwargs) -> List[CFR]:
    __delta = datetime.timedelta(days)
    loc = kwargs.get('location')
    if loc != None:
        loc = '202254' # id=202254 stands for LED SPb Pulkovo airport
    req = getReqInEBformat(pick_up, pick_up + __delta, loc=loc)

    async with session.post(url=url, headers=setHeaders(), json=req) as __r:
        st = await __r.status
        print(f"{url[:60]}.. Status code: ", st, "..")
        answ = await __r.content
        # if not __r.ok: return None
        answ = work_with_response(answ)
        if not verifyResponse(answ): return None

    return getData(res_list, answ.get('data').get('bcrm').get('carlist').get('cars'), days)