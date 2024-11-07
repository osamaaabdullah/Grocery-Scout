#import webdriver
from selenium import webdriver
#import By function
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

#import JSON data parser
from JSON_data_1 import add_item,write_file

#assign a driver variable
driver = webdriver.Chrome()

with open("product_url.txt", mode="r") as read_file:
    url_list = read_file.readlines()

for url in url_list:
    #navigating to a web page
    driver.get(url)
    
    #wait for the browser to load
    driver.implicitly_wait(10)
    
    
    try:
        #find the title and price by xpath
        find_title = driver.find_element(By.XPATH, "//*[@id='site-content']/div/div/div[2]/div[2]/div[2]/div/div/div[1]/h1")
        find_price = driver.find_element(By.XPATH, "//*[@id='site-content']/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div/div/span/span[1]")
        
        #Collect the data inside the tags
        title = find_title.text
        price_str = find_price.text
        price = float(price_str.replace('$',""))
        updated_item_dict = add_item('No Frills', url, title, price, 'available')
        
    #check if unavailable, gotta update stock later    
    except NoSuchElementException:
        continue
 
write_file('No Frills', updated_item_dict)    
driver.quit()