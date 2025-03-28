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
    
def scrape_product_details(driver):
    try:
        return {
            "url": driver.current_url,
            "title": driver.find_element(By.CSS_SELECTOR, "h1[itemprop='name']").text,
            "price": driver.find_element(By.CSS_SELECTOR, "span[itemprop='price']").text,
            "walmart_item_no": driver.find_element(By.XPATH, "//h3[text()='Walmart Item #']/following-sibling::div/span").text,
            "walmart_UPC": driver.find_element(By.XPATH, "//h3[text()='Universal Product Code (UPC check)']/following-sibling::div/span").text,
            "walmart_cat_ID": driver.find_element(By.XPATH, "//h3[text()='Category ID']/following-sibling::div/span").text,
            "walmart_SKU": driver.find_element(By.XPATH, "//h3[text()='SKU']/following-sibling::div/span").text,
            "lowest_price": "",
            "date_lowest_price": "" 
        }
    except NoSuchElementException:
        print("Exception")
        pass
                    
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
                    product_details = scrape_product_details(driver)
                    print(product_details)
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