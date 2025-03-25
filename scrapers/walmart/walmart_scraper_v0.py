from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from seleniumbase.common.exceptions import NoSuchElementException

import time

def click_element(driver,selector,button_found, exception_message):
    try:
        driver.click(selector)
        button_found = True
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        print(f"{exception_message}: {e}")

def scrape(url):
    driver = Driver(uc=True)
    try:
        driver.uc_open_with_reconnect(url, 4)
        driver.refresh()
        time.sleep(10)
        grocery_button_found, cookie_button_found = False, False
        landing_page_buttons = [('button[aria-label="close button"]', "Grocery button", grocery_button_found),('button[aria-label="Close Select the grocery link to find all grocery items."]', "Cookies button", cookie_button_found)]
        
        for selector, button_name,button in landing_page_buttons:
            click_element(driver, selector,button, f"{button_name} not found")
        
        if not (grocery_button_found and cookie_button_found):
            driver.refresh()
        
        # try:
        #     driver.click('button[aria-label="close button"]')
        # except NoSuchElementException:
        #     print("Grocery button not found")
        # except ElementClickInterceptedException:
        #     print("Grocery button not found")
        # try:
        #     driver.click('button[aria-label="Close dialogue"]')
        #     clicked_cookie_button = True    
        # except NoSuchElementException:
        #     print("Cookies button not found")
        # except ElementClickInterceptedException:
        #     print("Cookies button not found")
        # if (not(clicked_cookie_button)):
        #     try:
        #         driver.click('button[aria-label="Close Select the grocery link to find all grocery items."]')
        #     except NoSuchElementException:
        #         print("Cookies button not found")
        #     except ElementClickInterceptedException:
        #         print("Cookies button not found")
        driver.find_element("body").send_keys(Keys.PAGE_DOWN)
        number_of_pages = int((driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div[1]/main/div/div/div/div/div[4]/section/nav/ul/li[6]/div")).text)
        #driver.click('data-automation-id="fulfillment-banner"')
        time.sleep(5)
        no_of_elements = len(driver.find_elements(By.XPATH,"/html/body/div/div[1]/div/div[2]/div[1]/main/div/div/div/div/div[3]/div[2]/div/section/div/div"))
        for page in range(1,number_of_pages+1):
            for i in range(1,no_of_elements+1):
                try:
                    category_url = "/html/body/div/div[1]/div/div/div[1]/main/div/div/div/div/div[3]/div/div/section/div/div[" + str(i) + "]/div/div/a"
                    driver.click(category_url)
                    time.sleep(2)
                    try:
                        # title = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/div[2]/div[1]/section/main/div[2]/div[2]/div/div[1]/div/div/div[1]/div/div/div[1]/section/section[2]/h1")
                        # price = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/div[2]/div[1]/section/main/div[2]/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[1]/span[1]/span[2]/span")
                        title = driver.find_element(By.CSS_SELECTOR, "h1[itemprop='name']")
                        price = driver.find_element(By.CSS_SELECTOR, "span[itemprop='price']")
                        print(title.text,price.text)
                    except NoSuchElementException:
                        print("Exception")
                        pass
                except NoSuchElementException:
                    pass
                finally:
                    driver.back()
            time.sleep(5)
            driver.click('a[aria-label="Next Page"]')
    finally:
        driver.quit()
        
if __name__ == "__main__":
    
    url = "https://www.walmart.ca/en/browse/grocery/fruits-vegetables/10019_6000194327370?"
    scrape(url)
# print(number_of_pages)
# for i in range(2,int(number_of_pages)+1):
#     url = "https://www.walmart.ca/en/browse/grocery/fruits-vegetables/10019_6000194327370?page=" + str(i)
#     scrape(url)