from selenium import webdriver
from functions import *
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import xlsxwriter

## LAS VEGAS MARKET
class LVMActivity:
    def __init__(self,url):
        self.url = url
        self.array_current = 0
        self.array_href = []
        self.array_full_data = []
        pass

    def start_driver(self):
        self.driver = webdriver.Chrome('./chromedriver.exe')
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.start()
        pass

    def start(self):
        searchElement(self.driver,self.callback_filteredArray)

    def callback_filteredArray(self,array):
        self.array_of_elements = array
        self.array_max = len(array)
        self.scroll_to(array[self.array_current])
        array[self.array_current].click()
        getHrefs(self.driver,self.get_a,self)

    def back(self):
        self.driver.execute_script("window.history.go(-1)")

    def scroll_to(self,el):
        self.driver.execute_script("arguments[0].scrollIntoView();",el)

    def get_a(self,_array):
        self.array_current = self.array_current + 1

        if(self.array_current == self.array_max):
            self.array_href += _array
            self.write_to_excel_hrefs()
            print("HREFS wrote")
            view_link(self.array_href,self,self.driver)
            self.write_to_excel_datas()
            print("Whole Data wrote")
        else:
            self.array_href += _array
            self.back()
            WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"imc-campus-view--floor-name")))
            self.start()


    ## WRITE TO FULL DATA
    def write_to_excel_datas(self):
        workbook = xlsxwriter.Workbook("competitors_data_filtered.xlsx")
        worksheet = workbook.add_worksheet("Comp")
        row = 0
        col = 0

        worksheet.write(row,col,"Name")
        worksheet.write(row,col + 1,"Market Link")
        worksheet.write(row,col + 2,"Mattress / Adjustable")
        worksheet.write(row,col + 3,"Website URL")
        worksheet.write(row,col + 4,"Contact")

        worksheet.write(row,col + 5,"Product Notes")

        row += 1
        for i in self.array_full_data:
            worksheet.write(row,col,i["Name"])
            worksheet.write(row,col + 1, i["MarketLink"])
            worksheet.write(row,col + 2, i["categories"])
            worksheet.write(row,col + 3, i["website"])
            worksheet.write(row,col + 4,i["contact"])

            worksheet.write(row,col + 5, i["body"])
            row += 1

        workbook.close()




    def write_to_excel_hrefs(self):
        workbook = xlsxwriter.Workbook("possible_competitors_href.xlsx")
        worksheet = workbook.add_worksheet("Comp")
        row = 0
        col = 0

        worksheet.write(row,col,"Name")
        worksheet.write(row,col + 1,"Link")

        row +=1

        for i in self.array_href:
            worksheet.write(row,col,i['text'])
            worksheet.write(row,col+1,i['link'])
            row += 1

        workbook.close()

## HIGH POINT MARKET
class HPMActivity():
    def __init__(self,url):
        self.url = url

    def start_driver(self):
        self.driver = webdriver.Chrome('./chromedriver.exe')
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.start()


    def start(self):
        get_HPM_links(self.driver,self,self.filter_HPM_links)

    def filter_HPM_links(self,_arr):
        self.array_href = _arr
        self.write_to_excel_hrefs()
        filtered_arr = filter_HPM(self.driver,self,_arr)
        self.array_full_data = filtered_arr
        self.write_to_excel_datas()


    def back(self):
        self.driver.execute_script("window.history.go(-1)")

    def scroll_to(self,el):
        self.driver.execute_script("arguments[0].scrollIntoView();",el)

    def write_to_excel_hrefs(self):
        workbook = xlsxwriter.Workbook("possible_competitors_href_HVM.xlsx")
        worksheet = workbook.add_worksheet("Comp")
        row = 0
        col = 0

        worksheet.write(row,col,"Name")
        worksheet.write(row,col + 1,"Link")
        worksheet.write(row,col + 2,"Categories")


        row +=1

        for i in self.array_href:
            worksheet.write(row,col,i['text'])
            worksheet.write(row,col+1,i['link'])
            worksheet.write(row,col+2,i['categories'])

            row += 1

        workbook.close()

    def write_to_excel_datas(self):
        workbook = xlsxwriter.Workbook("competitors_data_filtered_HVM.xlsx")
        worksheet = workbook.add_worksheet("Comp")
        row = 0
        col = 0

        worksheet.write(row,col,"Name")
        worksheet.write(row,col + 1,"Market Link")
        worksheet.write(row,col + 2,"Mattress / Adjustable")
        worksheet.write(row,col + 3,"Website URL")
        worksheet.write(row,col + 4,"Contact")

        worksheet.write(row,col + 5,"Product Notes")

        row += 1
        for i in self.array_full_data:
            worksheet.write(row,col,i["Name"])
            worksheet.write(row,col + 1, i["MarketLink"])
            worksheet.write(row,col + 2, i["categories"])
            worksheet.write(row,col + 3, i["website"])
            worksheet.write(row,col + 4,i["contact"])

            worksheet.write(row,col + 5, i["body"])
            row += 1

        workbook.close()

class CustServicePortal():
    def __init__(self,url):
        self.url = url

    def start_driver(self):
        self.driver = webdriver.Chrome('./chromedriver.exe')
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.start()

    def start(self):
        set_login_site(self.driver,self,self.get_missing_link)

    def get_missing_link(self,pages):
        process_missing_links(self.driver,self,pages,self.print_to_excel)

    def scroll_to(self,el):
        self.driver.execute_script("arguments[0].scrollIntoView();",el)

    def print_to_excel(self,parts):
        workbook = xlsxwriter.Workbook("Parts With No Image.xlsx")
        worksheet = workbook.add_worksheet("Comp")
        row = 0
        col = 0

        worksheet.write(row,col,"Name")
        worksheet.write(row,col + 1,"Link")
        row +=1

        for i in parts:
            worksheet.write(row,col,i['name'])
            worksheet.write(row,col+1,i['link'])
            row += 1

        workbook.close()
