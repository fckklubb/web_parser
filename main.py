import datetime
import requests
from excel_funcs import AddRates, SaveExcel
from openpyxl.workbook import Workbook
from helpers import getAllRates as getAllRates

from config import DAYS

from rent_motors_parser import getOneColumnRates as rent_motors_func
from rex_rent_parser import getOneColumnRates as rex_rent_func
from a_arenda_parser import getOneColumnRates as a_arenda_func
from almak_parser import getOneColumnRates_almak as almak_func
from storlet_car_parser import getOneColumnRates as storlet_func

if __name__ == '__main__':
    with requests.Session() as s:
        
        for d in DAYS:
            print(f'>>> Rental start date after {d} days from taday..')
            pick_up = datetime.datetime.today() + datetime.timedelta(d)

            # SET UP EXCELL INFO SHEET
            wb = Workbook()
            ws = wb.active
            ws.title = "INFO"
            ws.cell(1, 1).value = "PARSER 1.0 by fckklubb"
            ws.cell(3, 1).value = f"Parsing date: {datetime.datetime.today().strftime('%d-%m-%Y')}"
            ws.cell(4, 1).value = f"Start date of a rental: {pick_up.strftime('%d-%m-%Y')}"
            ws.cell(6, 1).value = "Next companies are going to be parsed.."
            
            # Rent Motors
            print("1. Rent Motors..")
            ws.cell(8, 1).value = "RENT MOTORS"
            wb = AddRates("RENT-MOTORS", wb, getAllRates(pick_up, s, rent_motors_func, location=10))
            if wb == None:
                print("Panic.. Rent Motors failed..")

            # Rex Rent
            print("2. Rex Rent..")
            ws.cell(9, 1).value = "REX RENT"
            wb = AddRates("REX-RENT", wb, getAllRates(pick_up, s, rex_rent_func))
            if wb == None:
                print("Panic.. Rex Rent failed..")

            # A Arenda
            print("3. A Arenda..")
            ws.cell(10, 1).value = "A ARENDA"
            wb = AddRates("A-ARENDA", wb, getAllRates(pick_up, s, a_arenda_func))
            if wb == None:
                print("Panic.. A Arenda failed..")

            # Almak
            print("4. Almak..")
            ws.cell(11, 1).value = "ALMAK"
            wb = AddRates("ALMAK", wb, getAllRates(pick_up, s, almak_func, loop=False))
            if wb == None:
                print("Panic.. Almak failed..")

            # Storlet
            print("5. Storlet..")
            ws.cell(12, 1).value = "STORLET"
            wb = AddRates("STORLET", wb, getAllRates(pick_up, s, storlet_func))
            print("All done..")

            SaveExcel(wb, add_time=True)
        
        s.close()