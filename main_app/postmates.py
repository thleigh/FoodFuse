from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import datetime, re, requests, io, time, random, string
from bs4 import BeautifulSoup
import asyncio
from asgiref.sync import sync_to_async
import os

############# POSTMATES SELENIUM CODE (comments describing each step can be found on doordash.py) #############

# For Development
# from .chrome_driver import chrome_location
# options = Options()
# options.add_argument('--disable-extensions')
# options.add_argument('--window-size=800,600')
# options.add_argument('--proxy-byprass-list=*')
# options.add_argument('--start-maximized')
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')
# options.add_argument('--remote-debugging-port=9222')
# options.set_headless(True)

# driver = webdriver.Chrome(chrome_location, chrome_options=options)
#, chrome_options=options

# For production
chrome_options = Options()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--remote-debugging-port=9222')
chrome_options.add_argument('--window-size=800,600')
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


postmates_unparsed_list = []
postmates_main_url = []
async def postmates(data):
    try: 
        driver.get('https://postmates.com')
        await asyncio.sleep(5)
        print('on the PostMates Page!')

        address_link = driver.find_element_by_xpath('//*[@id="js-global-container"]/div/div[1]/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div[1]/input')
        address_button = driver.find_element_by_xpath('//*[@id="js-global-container"]/div/div[1]/div/div/div/div[1]/div/div[2]')

        address_link.click()
        await asyncio.sleep(0.5)
        address_link.send_keys(data)
        await asyncio.sleep(0.5)
        address_button.click()
        await asyncio.sleep(3)
        print('Going to PostMates Restaurant page')
    except:
        print ("First Link and Button Not Found on postmates")
        driver.close()

    try:
        restaurant_data = driver.find_elements_by_class_name('e12wrbia0')
    except:
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
        
        postmates_unparsed_list.append(parsed_text)

        # iterates through the unparsed_list and finds and removes where there is an empty array
        for item in postmates_unparsed_list: 
            if item == '':
                postmates_unparsed_list.remove(item)

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
    except:
        print ("Restaurant Link and Button Not Found on doordash")
        driver.close()

    try: 
        results = driver.find_element_by_class_name('css-mwpx6b')
    except:
        print ("Restaurant Data Not Found on doordash")
        driver.close()
    try: 
        text = results.text
        parsed_text = text.split('\n')

        postmates_restaurant_data.append(parsed_text)
    except:
        print ("Restaurant Data Not Found on doordash")
        driver.close()

    currentUrl = driver.current_url
    postmates_url.append(currentUrl)

    return data


@add_this_arg
def postmates_data_specific(this, data):
    if len(data) > 5:
        restaurant_name = data[3]
        delivery_data = data[0]
        delivery_time = data[5]
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

def pm_quit():
    driver.quit()
    print('pm driver quit')