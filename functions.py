from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def searchElement(driver,callback):
    WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CLASS_NAME,"imc-campus-view--floor-name")))

    a = driver.find_elements_by_class_name("imc-campus-view--floor-name")
    _filtered_array = []
    #print(a)
    for element in a:
        _el = element.find_elements(By.CLASS_NAME,"imc-campus-view-link")[0]
        #or _el.get_attribute('innerText') == "Furniture | Bedding"
        if(_el.get_attribute('innerText') == "Bedding"  or _el.get_attribute('innerText') == "Furniture | Bedding" ):
            _filtered_array.append(_el)

    callback(_filtered_array)


def getHrefs(driver,callback):
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
                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,"imc-button--primary-inverted")))
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
