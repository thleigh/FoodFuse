from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime, re, requests, io, time, random, string
from bs4 import BeautifulSoup
import asyncio
from asgiref.sync import sync_to_async
import os
# # Allows the chrome_driver to open without a physical browser
# chrome_options = Options()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
# #, chrome_options=options

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

ubereats_unparsed_list = []

async def ubereats(data):
    # Goes to Doordash Website
    driver.get('https://www.ubereats.com/')
    await asyncio.sleep(5)
    print('on the UberEats Page!')

    # # Finds the Address form and the Submit button by their XPATH
    address_link = driver.find_element_by_xpath('//*[@id="location-typeahead-home-input"]')
    address_button = driver.find_element_by_class_name('cv')

    # Clicks the address form
    address_link.click()
    await asyncio.sleep(0.5)
    # Input's the location into the form
    address_link.send_keys(data)
    await asyncio.sleep(0.5)
    # Clicks the submit button
    address_button.click()
    await asyncio.sleep(3)
    print('Goint to UberEats restaurant page')

    restaurant_data = driver.find_elements_by_class_name('g7')

    for i in range(len(restaurant_data[:])):
        each_restaurant = restaurant_data[:][i]
        text = each_restaurant.text
        parsed_text = text.split('\n')
        ubereats_unparsed_list.append(parsed_text)

    return ubereats_unparsed_list


def add_this_arg(func):
    def wrapped(*args, **kwargs):
        return func(wrapped, *args, **kwargs)
    return wrapped

@add_this_arg
def ubereats_data(this, data):
    restaurant_name = data[0]
    delivery_data = data[1]
    # delivery_time = data[3:]
    # delivery_cost = data[3]

    this.results = {
        'restaurant_name': restaurant_name,
        'delivery_data': delivery_data,
    }
    
    return data

ubereats_restaurant_data = []
def ubereatsRestaurant(data):
    restaurant_link = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/div[1]/div/div/div[1]/div/input')
    restaurant_link.send_keys(data)
    time.sleep(3)
    restaurant_link_inner = driver.find_element_by_class_name('css-70qvj9')
    restaurant_link_inner.click()
    time.sleep(3)
    print('on ubereats restaurant page!')

    results = driver.find_element_by_class_name('eifi54g6')

    text = results.text
    parsed_text = text.split('\n')

    ubereats_restaurant_data.append(parsed_text)

    return data


# @add_this_arg
# def ubereats_data_specific(this, data):
#     restaurant_name = data[3]
#     delivery_data = data[0]
#     delivery_time = data[5]
#     address = data[6]

#     this.results = {
#         'restaurant_name': restaurant_name,
#         'delivery_data': delivery_data,
#         'delivery_time': delivery_time,
#         'address': address,
#     }
#     return data