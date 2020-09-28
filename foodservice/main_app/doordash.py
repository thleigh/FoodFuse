from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime, re, requests, io, time, random, string
from bs4 import BeautifulSoup
# from main_app.views import location
from .chrome_driver import chrome_location

# Allows the chrome_driver to open without a physical browser
options = Options()
options.set_headless(True)

# locates the chrome_driver app in the local system
driver = webdriver.Chrome(chrome_location, chrome_options=options)

def doordash(data):
    # Goes to Doordash Website
    driver.get('https://www.doordash.com/en-US')
    time.sleep(5)
    print('on the Home Page!')

    # Finds the Address form and the Submit button by their XPATH
    address_link = driver.find_element_by_xpath('//input[starts-with(@id,"FieldWrapper")]')
    address_button = driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div/div/div/div/div/div/div[3]/div/button')

    # Clicks the address form
    address_link.click()
    time.sleep(0.5)
    # Input's the location into the form
    address_link.send_keys(data)
    time.sleep(0.5)
    # Clicks the submit button
    address_button.click()
    time.sleep(3)
    print('Going to address page')
    print('on the Restaurant page!')

    # Finds the DIV containing all of the restaurant data

    restaurant_data = driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[2]/div/div/div[1]/div[6]/div/div[2]').text
    restaurant_list = restaurant_data.split('\n')

    # Between the 0th and 7th index, append that range and repeat.
    # Between 0 and 7 is all of the info for one restaurant.
    final_list = []
    for i in range(0, len(restaurant_list), 7):
        final_list.append(restaurant_list[i:i+7])
        print(final_list)

