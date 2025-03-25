from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from seleniumbase.common.exceptions import NoSuchElementException

import time

def click_element(driver,selector,exception_message):
    """
    clicks the buttons to get rid of pop-ups in the initial load, handles exceptions if the pop-ups do not load.   
    """
    try:
        driver.click(selector)
        return True
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        print(f"{exception_message}: {e}")
        return False
def scrape(url):
    """
    scrapes walmart pages from the given url, url must be page that contains all items from a specific category.
    """
    driver = Driver(uc=True)
    try:
        driver.uc_open_with_reconnect(url, 4)
        driver.refresh()    #refresh the browser as a safety precaution for improper loading of pop-ups. Script does not behave as intended if the pop ups are not loaded properly.
        time.sleep(10)
        grocery_button_found, cookie_button_found = False, False    #placeholder to verify pop ups are loaded
        grocery_button_found = click_element(driver, 'button[aria-label="close button"]', "Grocery button not found")
        cookie_button_found = click_element(driver, 'button[aria-label="Close Select the grocery link to find all grocery items."]', "Cookies button not found")
        
        if not (grocery_button_found and cookie_button_found):
            driver.refresh()    #if pop ups are not loaded then refresh the page again to ensure script runs as intended
        driver.find_element("body").send_keys(Keys.PAGE_DOWN)   #scroll down the page to load the items
        number_of_pages = int((driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div[1]/main/div/div/div/div/div[4]/section/nav/ul/li[6]/div")).text)
        time.sleep(5)
        no_of_elements = len(driver.find_elements(By.XPATH,"/html/body/div/div[1]/div/div[2]/div[1]/main/div/div/div/div/div[3]/div[2]/div/section/div/div"))
        for page in range(1,number_of_pages+1):
            for i in range(1,no_of_elements+1):
                try:
                    category_url = "/html/body/div/div[1]/div/div/div[1]/main/div/div/div/div/div[3]/div/div/section/div/div[" + str(i) + "]/div/div/a"
                    driver.click(category_url)
                    time.sleep(2)
                    try:
                        title = driver.find_element(By.CSS_SELECTOR, "h1[itemprop='name']")
                        price = driver.find_element(By.CSS_SELECTOR, "span[itemprop='price']")
                        specifications_title = driver.find_elements(By.CSS_SELECTOR, "h3.flex")
                        specifications_subtitle = driver.find_elements(By.CSS_SELECTOR, "div.mv0")
                        print(specifications_title,specifications_subtitle)
                        for title,subtitle in zip(specifications_title,specifications_subtitle):
                            try:
                                print(title.text)
                                s_title = subtitle.find_element(By.TAG_NAME, "span")
                                print(s_title.text)    
                            except NoSuchElementException:
                                print("fail")
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