from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
import time

#### FOR LAS VEGAS MARKET
def searchElement(driver,callback):
    WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CLASS_NAME,"imc-campus-view--floor-name")))

    a = driver.find_elements_by_class_name("imc-campus-view--floor-name")
    _filtered_array = []
    #print(a)
    for element in a:
        _el = element.find_elements(By.CLASS_NAME,"imc-campus-view-link")[0]
        #or _el.get_attribute('innerText') == "Furniture | Bedding"
        #_el.get_attribute('innerText') == "Bedding"
        if(_el.get_attribute('innerText') == "Bedding"  or _el.get_attribute('innerText') == "Furniture | Bedding" ):
            _filtered_array.append(_el)

    callback(_filtered_array)


def getHrefs(driver,callback,context):
    try:
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"imc-type--title-5-link")))
        a = driver.find_elements(By.CLASS_NAME,"imc-type--title-5-link")
        _filtered_array = []
        count = 0
        for element in a:
            count += 1
            driver.execute_script("arguments[0].scrollIntoView();",element)
            x = {"text":element.get_attribute("innerText"),"link":element.get_attribute("href")}
            _filtered_array.append(x)
            #print(x)

        callback(_filtered_array)
        pass
    except TimeoutException:
        print ("Loading error!")
        callback([])
        pass

def view_link(array_href,context,driver):
    for _arr in array_href:
        driver.get(_arr["link"])
        try:
            info = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"imc-exhibitors-info")))
            context.scroll_to(info)

            body = "Description not available"
            categories = "Product Categories not available"
            site_link = "Link not available"
            contact = "No Contact"
            flag = 0

            try:
                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,"imc-type--body-1")))
                if len(driver.find_elements(By.CLASS_NAME,"imc-type--body-1")) > 0:
                    body = driver.find_elements(By.CLASS_NAME, "imc-type--body-1")[0].get_attribute("innerText")
            except TimeoutException:
                body = "Description not available"
                pass

            try:
                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,"imc-type--title-8")))
                if len(driver.find_elements(By.CLASS_NAME,"imc-type--title-8")) > 0:
                    categories = ""
                    cat_items = driver.find_elements(By.CLASS_NAME,"imc-type--title-8")
                    for i in cat_items:
                        if(i.get_attribute("innerText") == "Adjustable Beds" or i.get_attribute("innerText") == "Mattresses"):
                            categories += " / "
                            categories += i.get_attribute("innerText")
                            flag = 1

            except TimeoutException:
                categories = "Product Categories not available"
                pass

            try:
                WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CLASS_NAME,"imc-button--primary-inverted")))
                if len(driver.find_elements(By.CLASS_NAME,"imc-button--primary-inverted")) > 0:
                    link_button = driver.find_elements(By.CLASS_NAME,"imc-button--primary-inverted")
                    site_link = link_button[0].get_attribute("href")
                    if len(link_button) > 1:
                        site_link = link_button[1].get_attribute("href")

            except TimeoutException:
                site_link = "Link not available"

            try:
                contact_button = driver.find_elements(By.CLASS_NAME,"imc-button--contact-exhibitor")
                contact_button[0].click()
                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,"imc-contactexhibitormodal--body-panel")))

                contact_dialog = driver.find_elements(By.CLASS_NAME,"imc-contactexhibitormodal--body-panel")

                #texts = contact_dialog[0].find_elements(By.CLASS_NAME,"imc-type--title-3-ui")
                #print(texts)

                texts = contact_dialog[1].find_elements(By.CLASS_NAME,"imc-type--title-3-ui");
                contact =  ""
                for i in texts:
                    if(i.get_attribute("innerText") == "Phone"):
                        contact += "Phone: \n\n"
                    elif(i.get_attribute("innerText") == "Showroom Contact"):
                        contact += "Showroom Contact: \n\n"
                    elif(i.get_attribute("innerText") == "Follow Us"):
                        contact += ""
                    else:
                        contact += i.get_attribute("innerText")
                        contact += " \n"


            except TimeoutException:
                contact = "No Contact"






            #if len(driver.find_elements(By.CLASS_NAME,"imc-button--primary-inverted")) > 0:
            new_data = {"Name":_arr['text'],"MarketLink":_arr["link"],"body":body,"categories":categories,"website":site_link,"contact":contact}
            if(flag):
                context.array_full_data.append(new_data)




        except TimeoutException:
            print("Error viewing page")

###### FOR HIGH POINT MARKET
def get_HPM_links(driver,context,callback):
    href_data = []
    href_data += set_adjustable(driver,context)
    context.back()
    href_data += set_mattresses(driver,context,href_data)
    callback(href_data)

    #cat4[0].click()

def set_mattresses(driver,context,adj_data):
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"cd-dropdown-trigger")))

    href_data = []

    filter = driver.find_elements(By.CLASS_NAME,"cd-dropdown-trigger")
    search = driver.find_elements(By.CLASS_NAME,"search")

    filter[0].click()
    categories = driver.find_elements(By.CLASS_NAME,"has-children.outer")
    #context.scroll_to(categories[0])

    time.sleep(2)

    categories[0].click()


    time.sleep(2)
    cat1 = categories[0].find_elements(By.XPATH,"./ul/li")
    body = categories[0].find_elements(By.XPATH,"./ul")
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", body[0])
    time.sleep(5)
    cat1[14].click()
  # TODO:
    time.sleep(10)
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"exh-name")))
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CLASS_NAME,"exh-name")))

    exhibitor = driver.find_elements(By.CLASS_NAME,"exh-name")
    for item in exhibitor:
        a = item.find_elements(By.XPATH,"./../..")
        add = 1
        for i in adj_data:
            if(i['text'] == item.get_attribute("innerText")):
                i["categories"] += "/ Mattresses"
                add = 0
                break
        if(add):
            data = {'text':item.get_attribute("innerText"),'link':a[0].get_attribute("href"),'categories':"Mattresses"}
            href_data.append(data)


    return href_data


def set_adjustable(driver,context):
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"cd-dropdown-trigger")))

    href_data = []

    filter = driver.find_elements(By.CLASS_NAME,"cd-dropdown-trigger")
    context.scroll_to(filter[0])
    filter[0].click()

    categories = driver.find_elements(By.CLASS_NAME,"has-children.outer")
    time.sleep(1)

    categories[0].click()

    categories2 = categories[0].find_elements(By.CLASS_NAME,"has-children")
    time.sleep(1)
    categories2[3].click()

    categories3 = categories2[3].find_elements(By.XPATH,"//ul[@class='innerlist']/li")

    cat4 = categories3[2].find_elements(By.CLASS_NAME,"filterLink.c")
    WebDriverWait(driver,10).until(EC.element_to_be_clickable(cat4[0]))
    #WebDriverWait(driver,10).until(EC.presence_of_element_located(cat4[0]))
    time.sleep(5)
    cat4[0].click()

    time.sleep(10)
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"exh-name")))
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CLASS_NAME,"exh-name")))

    exhibitor = driver.find_elements(By.CLASS_NAME,"exh-name")
    for item in exhibitor:
        context.scroll_to(item)
        a = item.find_elements(By.XPATH,"./../..")
        data = {'text':item.get_attribute("innerText"),'link':a[0].get_attribute("href"),'categories':"Adjustable Bed"}
        href_data.append(data)

    return href_data

def filter_HPM(driver,context,_arr):
    newarr = []
    for i in _arr:
        driver.get(i['link'])
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"exh-info")))
        time.sleep(1)

        con1 = driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblLocation")
        con2 = driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblBusStop")
        con3 = driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblNeighborhood")
        con4 = driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblCorpPhone")
        web = driver.find_element_by_id("ctl00_ContentPlaceHolder1_lnkWebsite")

        contact =""
        contact += con1.get_attribute("innerText")
        contact += "\n"
        contact += con2.get_attribute("innerText")
        contact += "\n"
        contact += con3.get_attribute("innerText")
        contact += "\n"
        contact += con4.get_attribute("innerText")

        weblink = web.get_attribute("href")
        categories = i['categories']
        about = ""
        try:
            WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_lblDescription")))
            about = driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblDescription").get_attribute("innerText")
        except TimeoutException:
            about = "NONE"

        new_data = {"Name":i['text'],"MarketLink":i["link"],"body":about,"categories":categories,"website":weblink,"contact":contact}
        newarr.append(new_data)
        context.back()
        time.sleep(2)

    return newarr
