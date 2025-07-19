from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from seleniumbase.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import time

# def click_element(driver,selector,exception_message):
#     """
#     clicks the buttons to get rid of pop-ups in the initial load, handles exceptions if the pop-ups do not load.   
#     """
#     try:
#         driver.click(selector)
#         return True
#     except (NoSuchElementException, ElementClickInterceptedException) as e:
#         print(f"{exception_message}: {e}")
#         return False
    
# def scrape_product_details(driver):
#     try:
#         WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1[class='pi--title']")))
#         return {
#             "url": driver.current_url,
#             "title": driver.find_element(By.CSS_SELECTOR, "h1[class='pi--title']").text,
#             "price": driver.find_element(By.CSS_SELECTOR, "span.price-update").text,
#             "lowest_price": "",
#             "date_lowest_price": "" 
#         }
#     except:
#         print("Exception")
#         pass
                    
# def scrape(url):
#     """
#     scrapes walmart pages from the given url, url must be page that contains all items from a specific category.
#     """
#     driver = Driver(uc=True)
#     try:
#         driver.uc_open_with_reconnect(url, 4)
#         driver.refresh()    #refresh the browser as a safety precaution for improper loading of pop-ups. Script does not behave as intended if the pop ups are not loaded properly.
#         time.sleep(10)
#         driver.find_element("body").send_keys(Keys.PAGE_DOWN)   #scroll down the page to load the items
#         number_of_pages = int((driver.find_element(By.XPATH, "/html/body/div[1]/div[9]/div[2]/div[2]/div[3]/div/div/div/div[1]/div[4]/div[4]/div/div/a[6]")).text)
#         time.sleep(5)
#         no_of_elements = len(driver.find_elements(By.CSS_SELECTOR, "div.default-product-tile"))
#         for page in range(1,number_of_pages+1):
#             if(page!=1):
#                 time.sleep(60)
#             for i in range(1,no_of_elements+1):
#                 try:
#                     category_url = "/html/body/div[1]/div[9]/div[2]/div[2]/div[3]/div/div/div/div[1]/div[4]/div[3]/div/div[" + str(i) + "]/div[1]/a"
#                     driver.click(category_url)
#                     product_details = scrape_product_details(driver)
#                     print(product_details)
#                     driver.back()
#                 except (ElementNotInteractableException, NoSuchElementException):
#                     pass                    
#             time.sleep(5)
#             driver.click('a[aria-label="Next Page"]')
#     finally:
#         driver.quit()
        
if __name__ == "__main__":
    
    url = "https://www.metro.ca/en/online-grocery/themed-baskets/local-products/grocery"
    scrape(url)
    
    
    