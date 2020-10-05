from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import datetime, re, requests, io, time, random, string
from bs4 import BeautifulSoup
import asyncio
from asgiref.sync import sync_to_async
import os

# Allows the chrome_driver to open without a physical browser
# chrome_options = Options()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

from .chrome_driver import chrome_location
options = Options()
options.add_argument('--disable-extensions')
options.add_argument('--window-size=1920,1080')
options.add_argument('--proxy-byprass-list=*')
options.add_argument('--start-maximized')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.set_headless(True)

# locates the chrome_driver app in the local system
driver = webdriver.Chrome(chrome_location, chrome_options=options)
#, chrome_options=options

doordash_unparsed_list = []

async def doordash(data):
    # Goes to Doordash Website
    try: 
        driver.get('https://www.doordash.com/en-US')
        await asyncio.sleep(5)
        print('on the Doordash Home Page!')

        # Finds the Address form and the Submit button by their XPATH
        address_link = driver.find_element_by_xpath('//input[starts-with(@id,"FieldWrapper")]')
        address_button = driver.find_element_by_class_name('sc-eCXBzT')

        # Clicks the address form
        address_link.click()
        await asyncio.sleep(0.5)
        # Input's the location into the form
        address_link.send_keys(data)
        await asyncio.sleep(0.5)
        # Clicks the submit button
        address_button.click()
        await asyncio.sleep(5)
        print('Going to Doordash Restaurant page')
    except TimeoutException:
        print ("First Link and Button Not Found on doordash")
        driver.close()

    # Finds the DIV containing all of the restaurant data
    try:
        restaurant_data = driver.find_elements_by_class_name('sc-boCWhm')
        # print(restaurant_data)
    except TimeoutException:
        print ("Data Not Found on doordash")
        driver.close()

    for names in restaurant_data:
        text = names.text
        parsed_text = text.split('\n')
        if "Currently Closed" in parsed_text:
            pass
        else:
            doordash_unparsed_list.append(parsed_text)
    return doordash_unparsed_list

def add_this_arg(func):
    def wrapped(*args, **kwargs):
        return func(wrapped, *args, **kwargs)
    return wrapped

@add_this_arg
def doordash_data(this, data):
    restaurant_name = data[0]
    pricing = data[1]
    categories = data[2]
    delivery_time = data[3]
    if "Newly Added" in data: 
        # rating = data[4]
        delivery_cost = data[5]
    else:
        # rating = " ".join(data[4:5])
        delivery_cost = data[6]
        
    this.results = {
        'restaurant_name': restaurant_name,
        'pricing': pricing,
        'categories': categories,
        'delivery_time': delivery_time,
        # 'rating': rating,
        'delivery_cost': delivery_cost,
    }
    return data

doordash_restaurant_data = []
def doordashRestaurant(data):
    try:
        restaurant_link = driver.find_element_by_class_name('sc-ewMkZo')
        restaurant_link.send_keys(data)
        time.sleep(3)
        restaurant_link_inner = driver.find_element_by_class_name('sc-fjmCvl')
        # //*[@id="search-dropdown-results"]/a[1]
        restaurant_link_inner.click()
        time.sleep(3)
        print('on restaurant page!')
    except TimeoutException:
        print ("Restaurant Link and Button Not Found on doordash")
        driver.close()

    try:
        results = driver.find_element_by_class_name('sc-eitiEO')
    except TimeoutException:
        print ("Restaurant Data Not Found on doordash")
        driver.close()

    text = results.text
    parsed_text = text.split('\n')

    doordash_restaurant_data.append(parsed_text)

    return data


@add_this_arg
def doordash_data_specific(this, data):
    restaurant_name = data[0]
    delivery_data = data[10]
    delivery_time = data[12]
    # address = data[9]

    this.results = {
        'restaurant_name': restaurant_name,
        'delivery_data': delivery_data,
        'delivery_time': delivery_time,
        # 'address': address,
    }
    driver.quit()
    return data