from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime, re, requests, io, time, random, string
from bs4 import BeautifulSoup
from .chrome_driver import chrome_location

# Allows the chrome_driver to open without a physical browser
options = Options()
options.add_argument('--disable-extensions')
options.add_argument('--window-size=1920,1080')
# options.add_argument("--proxy-server='direct://'")
options.add_argument('--proxy-byprass-list=*')
options.add_argument('--start-maximized')
options.add_argument('--disable-gpu')
# options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
# options.add_argument('--ignore-certificate-errors')

options.set_headless(True)

# locates the chrome_driver app in the local system
driver = webdriver.Chrome(chrome_location, chrome_options=options)
# , chrome_options=options

postmates_unparsed_list = []
def postmates(data):
    # Goes to Doordash Website
    driver.get('https://postmates.com')
    time.sleep(5)
    print('on the PostMates Page!')

    # Finds the Address form and the Submit button by their XPATH
    address_link = driver.find_element_by_xpath('//*[@id="js-global-container"]/div/div[1]/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div[1]/input')
    address_button = driver.find_element_by_xpath('//*[@id="js-global-container"]/div/div[1]/div/div/div/div[1]/div/div[2]')

    # # Clicks the address form
    address_link.click()
    time.sleep(0.5)
    # Input's the location into the form
    address_link.send_keys(data)
    time.sleep(0.5)
    # Clicks the submit button
    address_button.click()
    time.sleep(3)
    print('Going to PostMates Restaurant page')

    restaurant_data = driver.find_elements_by_class_name('e12wrbia0')
    # print(restaurant_data)

    for names in restaurant_data:
        text = names.text
        parsed_text = text.split('\n')
        if '' in parsed_text:
            parsed_text.remove('')
        if "ONLY ON POSTMATES" in parsed_text:
            parsed_text.remove("ONLY ON POSTMATES")
            # " ".join(parsed_text)
        if "$3 OFF $15" in parsed_text:
            parsed_text.remove("$3 OFF $15")
        if "MINIMUM $15" in parsed_text:
            parsed_text.remove("MINIMUM $15")
        if "INFATUATION APPROVED" in parsed_text:
            parsed_text.remove("INFATUATION APPROVED")
            # " ".join(parsed_text)
        if "POPULAR" in parsed_text:
            parsed_text.remove("POPULAR")
            # " ".join(parsed_text)
        if "OCEAN FRIENDLY" in parsed_text:
            parsed_text.remove("OCEAN FRIENDLY")
            # " ".join(parsed_text)
        if "NEW" in parsed_text:
            parsed_text.remove("NEW")
            # " ".join(parsed_text)
        if "Available Later" in parsed_text:
            pass
        if '·' in parsed_text:
            parsed_text.remove('')

        # joined_text = " ".join(parsed_text)
        postmates_unparsed_list.append(parsed_text)

        for item in postmates_unparsed_list: 
            if item == '':
                postmates_unparsed_list.remove(item)
    return postmates_unparsed_list

def add_this_arg(func):
    def wrapped(*args, **kwargs):
        return func(wrapped, *args, **kwargs)
    return wrapped

@add_this_arg
def postmates_data(this, data):
    restaurant_name = data[0]
    delivery_data = data[1]
    # delivery_time = data[i][2]
    # categories = data[i][2]
    # delivery_cost = data[i][3]
    # rating = data[i][4]

    this.results = {
        'restaurant_name': restaurant_name,
        # 'pricing': pricing,
        # 'categories': categories,
        'delivery_data': delivery_data,
        # 'rating': rating,
        # 'rating_amt': rating_amt,
        # 'delivery_cost': delivery_cost,
    }
    return data



