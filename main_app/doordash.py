from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import datetime, re, requests, io, time, random, string
from bs4 import BeautifulSoup
import asyncio
from asgiref.sync import sync_to_async
import os


############# DOORDASH SELENIUM CODE #############

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
doordash_unparsed_list = []
# List to store the site's url of the first search
doordash_main_url = []
async def doordash(data):
    # Goes to Doordash Website
    # Tests to see if these elements exist, if not, close the webdriver.
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
    except:
        print ("First Link and Button Not Found on doordash")
        driver.close()

    # Finds the DIV containing all of the restaurant data
    try:
        restaurant_data = driver.find_elements_by_class_name('sc-boCWhm')
    except:
        print ("Data Not Found on doordash")
        driver.close()

    # Iterates through the restaurant_data list and creates more detailed results
    for names in restaurant_data:
        text = names.text
        parsed_text = text.split('\n')
        if "Currently Closed" in parsed_text:
            pass
        else:
            doordash_unparsed_list.append(parsed_text)

    # gets the url of the current page and appends it to the main_url list
    currentUrl = driver.current_url
    doordash_main_url.append(currentUrl)

    return doordash_unparsed_list

# Function used to add 'this'
def add_this_arg(func):
    def wrapped(*args, **kwargs):
        return func(wrapped, *args, **kwargs)
    return wrapped

# Takes the unparsed_data list and assigns each index to a variable
@add_this_arg
def doordash_data(this, data):
    if len(data) > 5:
        restaurant_name = data[0]
        delivery_time = data[3]
        if "Newly Added" in data: 
            delivery_cost = data[5]
        else:
            delivery_cost = data[6]
    else: 
        restaurant_name = 'No data found.'
        delivery_time = None
        delivery_cost = None
        
    this.results = {
        'restaurant_name': restaurant_name,
        'delivery_time': delivery_time,
        'delivery_cost': delivery_cost,
    }
    return data

doordash_restaurant_data = []
doordash_url = []
def doordashRestaurant(data):
    try:
        # Finds the input at the top of the page
        restaurant_link = driver.find_element_by_class_name('sc-ewMkZo')
        # Inputs the restaurant data that the user submits
        restaurant_link.send_keys(data)
        time.sleep(3)
        # Finds the popup hover once there is data inserted into the input and clicks that hover
        restaurant_link_inner = driver.find_element_by_class_name('sc-fjmCvl')
        restaurant_link_inner.click()
        time.sleep(3)
        print('on restaurant page!')
    except:
        print ("Restaurant Link and Button Not Found on doordash")
        driver.close()

    try:
        # Gets the data on the specific restaurant page
        results = driver.find_element_by_class_name('sc-eitiEO')
    except:
        print ("Restaurant Data Not Found on doordash")
        driver.close()

    text = results.text
    parsed_text = text.split('\n')

    doordash_restaurant_data.append(parsed_text)

    # Gets the URL of the current Restaurant and appends that to the url list
    currentUrl = driver.current_url
    doordash_url.append(currentUrl)

    return data


@add_this_arg
def doordash_data_specific(this, data):
    if len(data) > 0:
        restaurant_name = data[0]
        delivery_data = data[9]
        delivery_time = data[11:12]
    else: 
        restaurant_name = 'No Data found, Please Try Again.'
        delivery_data = 'No Data found, Please Try Again.'
        delivery_time = 'No Data found, Please Try Again.'    

    this.results = {
        'restaurant_name': restaurant_name,
        'delivery_data': delivery_data,
        'delivery_time': delivery_time,
    }
    driver.close()
    return data

def dd_quit():
    driver.quit()
    print('dd driver quit')