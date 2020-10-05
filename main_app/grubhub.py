# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import datetime, re, requests, io, time, random, string
# from bs4 import BeautifulSoup
# from .chrome_driver import chrome_location
# import asyncio
# from asgiref.sync import sync_to_async

# options = Options()
# options.add_argument('--disable-extensions')
# options.add_argument('--window-size=1920,1080')
# options.add_argument('--proxy-byprass-list=*')
# options.add_argument('--start-maximized')
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')
# options.set_headless(True)

# driver = webdriver.Chrome(chrome_location, chrome_options=options)
# # , chrome_options=options

# grubhub_unparsed_list = []

# async def grubhub(data):
#     driver.get('https://grubhub.com')
#     await asyncio.sleep(5)
#     print('on the Grubhub Page!')

#     address_link = driver.find_element_by_xpath('//*[@id="homepage-logged-out-top"]/ghs-welcome-view/div/div[2]/div[2]/div[2]/ghs-start-order-form/div/div[1]/div/ghs-address-input/div/div/div/input')
#     address_button = driver.find_element_by_class_name('addressInput-submitBtn')

#     address_link.click()
#     await asyncio.sleep(0.5)
#     address_link.send_keys(data)
#     await asyncio.sleep(0.5)
#     address_button.click()
#     await asyncio.sleep(3)
#     print('Going to Grubhub Restaurant page!')

#     restaurant_data = driver.find_elements_by_class_name('searchResult')

#     for names in restaurant_data:
#         text = names.text
#         parsed_text = text.split('\n')
#         if '' in parsed_text:
#             parsed_text.remove('')
#         if "Featured" in parsed_text:
#             parsed_text.remove("Featured")
#         if "$4 for $4 Meal Deals" in parsed_text:
#             parsed_text.remove("$4 for $4 Meal Deals")
#         if "Closing soon. Order before" in parsed_text:
#             parsed_text.remove("Closing soon. Order before")[0:]
#         if "off your order" in parsed_text:
#             parsed_text.remove("off your order")
#         if "New" in parsed_text:
#             parsed_text.remove("New")

#         grubhub_unparsed_list.append(parsed_text)

#     return grubhub_unparsed_list

# def add_this_arg(func):
#     def wrapped(*args, **kwargs):
#         return func(wrapped, *args, **kwargs)
#     return wrapped

# @add_this_arg
# def grubhub_data(this, data):
#     restaurant_name = data[0]
#     delivery_time = data[3:]

#     this.results = {
#         'restaurant_name': restaurant_name,
#         'delivery_time': delivery_time,
#     }
    
#     return data




