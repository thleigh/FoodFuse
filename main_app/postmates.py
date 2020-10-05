from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import datetime, re, requests, io, time, random, string
from bs4 import BeautifulSoup
import asyncio
from asgiref.sync import sync_to_async
import os

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

# List to store inital data
postmates_unparsed_list = []
# List to store the site's url of the first search
postmates_main_url = []
async def postmates(data):
    # Goes to Doordash Website
    # Tests to see if these elements exist, if not, close the webdriver.
    try: 
        driver.get('https://postmates.com')
        await asyncio.sleep(5)
        print('on the PostMates Page!')

        # Finds the Address form and the Submit button by their XPATH
        address_link = driver.find_element_by_xpath('//*[@id="js-global-container"]/div/div[1]/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div[1]/input')
        address_button = driver.find_element_by_xpath('//*[@id="js-global-container"]/div/div[1]/div/div/div/div[1]/div/div[2]')

        # # Clicks the address form
        address_link.click()
        await asyncio.sleep(0.5)
        # Input's the location into the form
        address_link.send_keys(data)
        await asyncio.sleep(0.5)
        # Clicks the submit button
        address_button.click()
        await asyncio.sleep(3)
        print('Going to PostMates Restaurant page')
    except TimeoutException:
        print ("First Link and Button Not Found on postmates")
        driver.close()

    try:
        restaurant_data = driver.find_elements_by_class_name('e12wrbia0')
    except TimeoutException:
        print ("Data Not Found on doordash")
        driver.close()

    for names in restaurant_data:
        text = names.text
        parsed_text = text.split('\n')
        if '' in parsed_text:
            parsed_text.remove('')
        if "ONLY ON POSTMATES" in parsed_text:
            parsed_text.remove("ONLY ON POSTMATES")
        if "$3 OFF $15" in parsed_text:
            parsed_text.remove("$3 OFF $15")
        if "MINIMUM $15" in parsed_text:
            parsed_text.remove("MINIMUM $15")
        if "INFATUATION APPROVED" in parsed_text:
            parsed_text.remove("INFATUATION APPROVED")
        if "POPULAR" in parsed_text:
            parsed_text.remove("POPULAR")
        if "OCEAN FRIENDLY" in parsed_text:
            parsed_text.remove("OCEAN FRIENDLY")
        if "NEW" in parsed_text:
            parsed_text.remove("NEW")
        if 'Available Later' in parsed_text:
            parsed_text.remove('Available Later')
        if 'Too Busy' in parsed_text:
            parsed_text.remove('Too Busy')
        if 'Alcohol' in parsed_text:
            parsed_text.remove('Alcohol')

        # for x in parsed_text:
        #     temp = x[1].split('·')
        #     x[1] = temp[0]
        #     x.append(temp[1])
        
        postmates_unparsed_list.append(parsed_text)

        for item in postmates_unparsed_list: 
            # item.split('·')
            if item == '':
                postmates_unparsed_list.remove(item)

    # gets the url of the current page and appends it to the main_url list
    currentUrl = driver.current_url
    postmates_main_url.append(currentUrl)

    return postmates_unparsed_list

def add_this_arg(func):
    def wrapped(*args, **kwargs):
        return func(wrapped, *args, **kwargs)
    return wrapped

@add_this_arg
def postmates_data(this, data):
    restaurant_name = data[0]
    delivery_data = data[1]

    this.results = {
        'restaurant_name': restaurant_name,
        'delivery_data': delivery_data,
    }
    return data

postmates_restaurant_data = []
postmates_url = []
def postmatesRestaurant(data):
    try:
        restaurant_link = driver.find_element_by_class_name('css-nzssee')
        restaurant_link.send_keys(data)
        time.sleep(3)
        restaurant_link_inner = driver.find_element_by_class_name('css-1d3pcta')
        restaurant_link_inner.click()
        time.sleep(3)
        print('on Postmates page!')
    except TimeoutException:
        print ("Restaurant Link and Button Not Found on doordash")
        driver.close()

    try: 
        results = driver.find_element_by_class_name('css-mwpx6b')
    except TimeoutException:
        print ("Restaurant Data Not Found on doordash")
        driver.close()

    text = results.text
    parsed_text = text.split('\n')

    postmates_restaurant_data.append(parsed_text)

    currentUrl = driver.current_url
    postmates_url.append(currentUrl)

    return data


@add_this_arg
def postmates_data_specific(this, data):
    restaurant_name = data[3]
    delivery_data = data[0]
    delivery_time = data[6]
    # address = data[8]

    this.results = {
        'restaurant_name': restaurant_name,
        'delivery_data': delivery_data,
        'delivery_time': delivery_time,
        # 'address': address,
    }
    driver.quit()
    return data