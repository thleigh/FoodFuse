from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import datetime, re, requests, io, time, random, string
from bs4 import BeautifulSoup
import asyncio
from asgiref.sync import sync_to_async
import os

# For development
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

# For production
# chrome_options = Options()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


# List to store inital data
ubereats_unparsed_list = []
# List to store the site's url of the first search
ubereats_main_url = []
async def ubereats(data):
    # Goes to Doordash Website
    # Tests to see if these elements exist, if not, close the webdriver.    
    try:
        driver.get('https://www.ubereats.com/')
        await asyncio.sleep(5)
        print('on the UberEats Page!')

        # Finds the Address form and the Submit button by their XPATH
        address_link = driver.find_element_by_name('searchTerm')
        address_button = driver.find_element_by_class_name('dg')
        # Clicks the address form
        address_link.click()
        await asyncio.sleep(0.5)
        # Input's the location into the form
        address_link.send_keys(data)
        await asyncio.sleep(0.5)
        # Clicks the submit button
        address_button.click()
        await asyncio.sleep(5)
        print('Goint to UberEats restaurant page')
    except TimeoutException:
        print ("First Link and Button Not Found on Ubereats")
        driver.close()

    try:
        restaurant_data = driver.find_elements_by_class_name('g3')
    except TimeoutException:
        print ("Initial Data Not Found on Ubereats")
        driver.close()

    for i in range(len(restaurant_data[:])):
        each_restaurant = restaurant_data[:][i]
        text = each_restaurant.text
        parsed_text = text.split('\n')
        ubereats_unparsed_list.append(parsed_text)

    # gets the url of the current page and appends it to the main_url list
    currentUrl = driver.current_url
    ubereats_main_url.append(currentUrl)

    return ubereats_unparsed_list


def add_this_arg(func):
    def wrapped(*args, **kwargs):
        return func(wrapped, *args, **kwargs)
    return wrapped

@add_this_arg
def ubereats_data(this, data):
    if len(data) > 0:
        restaurant_name = data[0]
        delivery_data = f'{data[2]} · {data[5]}'
    else: 
        restaurant_name = 'No Data Found, Please Try again.'

    this.results = {
        'restaurant_name': restaurant_name,
        'delivery_data': delivery_data,
    }
    
    return data

ubereats_restaurant_data = []
ubereats_url = []
def ubereatsRestaurant(data):
    time.sleep(3)
    try: 
        restaurant_link = driver.find_element_by_class_name('d4')
        restaurant_link.click()
        restaurant_link.send_keys(data)
        time.sleep(3)
        restaurant_link_inner = driver.find_element_by_xpath('//*[@id="search-suggestions-typeahead-item-0"]')
        restaurant_link_inner.click()
        time.sleep(3)
        print('on ubereats restaurant page!')
    except TimeoutException:
        print ("Restaurant Link and Button Not Found on Ubereats")
        driver.close()
    try:
        results = driver.find_element_by_xpath('//*[@id="wrapper"]/main/div[2]/div/div/div[2]/div/div[2]/div[1]')
    except TimeoutException:
        print ("Restaurant Not Found on Ubereats")
        driver.close()

    text = results.text
    parsed_text = text.split('\n')

    ubereats_restaurant_data.append(parsed_text)

    currentUrl = driver.current_url
    ubereats_url.append(currentUrl)

    return data


@add_this_arg
def ubereats_data_specific(this, data):
    if len(data) > 2:
        delivery_data = data[6]
        delivery_time = data[1]
    else:
        delivery_data = 'No Data Found, Please Try Again.'

    this.results = {
        'delivery_data': delivery_data,
        'delivery_time': delivery_time,
    }
    driver.quit()
    return data