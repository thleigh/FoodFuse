from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime, re, requests, io, time, random, string
from bs4 import BeautifulSoup
# from main_app.views import location
from .chrome_driver import chrome_location

# Allows the chrome_driver to open without a physical browser
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

options.set_headless(True)

# locates the chrome_driver app in the local system
driver = webdriver.Chrome(chrome_location, chrome_options=options)
#, chrome_options=options

final_list = []

def doordash(data):
    # Goes to Doordash Website
    driver.get('https://www.doordash.com/en-US')
    time.sleep(5)
    print('on the Home Page!')

    # Finds the Address form and the Submit button by their XPATH
    address_link = driver.find_element_by_xpath('//input[starts-with(@id,"FieldWrapper")]')
    address_button = driver.find_element_by_class_name('sc-jFpLkX')

    # Clicks the address form
    address_link.click()
    time.sleep(0.5)
    # Input's the location into the form
    address_link.send_keys(data)
    time.sleep(0.5)
    # Clicks the submit button
    address_button.click()
    time.sleep(5)
    print('Going to address page')
    print('on the Restaurant page!')

    # Finds the DIV containing all of the restaurant data
    restaurant_data = driver.find_elements_by_class_name('sc-boCWhm')
    for names in restaurant_data:
        text = names.text
        parsed_text = text.split('\n')
        if "Currently Closed" in parsed_text:
            pass
        else:
            final_list.append(parsed_text)

    return final_list

def add_this_arg(func):
    def wrapped(*args, **kwargs):
        return func(wrapped, *args, **kwargs)
    return wrapped

@add_this_arg
def parsed_data(this, data):
    restaurant_name = data[0]
    pricing = data[1]
    categories = data[2]
    delivery_time = data[3]
    if "Newly Added" in data: 
        rating = data[4]
        delivery_cost = data[5]
    else:
        rating = " ".join(data[4:5])
        delivery_cost = data[6]
        
    this.results = {
        'restaurant_name': restaurant_name,
        'pricing': pricing,
        'categories': categories,
        'delivery_time': delivery_time,
        'rating': rating,
        # 'rating_amt': rating_amt,
        'delivery_cost': delivery_cost,
    }
    return data


    # rating_amt = final_list[i][5]
    # delivery_cost = final_list[i][6]


    #favorite_button 