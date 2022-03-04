from selenium import webdriver
from functions import *
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import xlsxwriter

class Activity:
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
        getHrefs(self.driver,self.get_a)

    def back(self):
        self.driver.execute_script("window.history.go(-1)")

    def scroll_to(self,el):
        self.driver.execute_script("arguments[0].scrollIntoView();",el)

    def get_a(self,_array):
        self.array_current = self.array_current + 1
        if(self.array_current == self.array_max):
            #self.write_to_excel_hrefs()
            #self.driver.get("https://www.lasvegasmarket.com/exhibitor/90910'")
            #time.sleep(10)
            view_link(self.array_href,self,self.driver)
            #print(self.array_full_data)
            print(self.array_full_data)
            self.write_to_excel_datas()
        else:
            self.array_href += _array
            self.back()
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"imc-campus-view--floor-name")))
            self.start()

    ## WRITE TO FULL DATA
    def write_to_excel_datas(self):
        workbook = xlsxwriter.Workbook("competitors_data.xlsx")
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
        workbook = xlsxwriter.Workbook("competitors.xlsx")
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





def main():
    activity = Activity("https://www.lasvegasmarket.com/Market%20Map/")
    activity.start_driver()


if __name__ == '__main__':
    main()
