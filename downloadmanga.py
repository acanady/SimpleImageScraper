import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import base64
import time
import os
import json

def FindImages(webpage_url):

    folder_path = "Images" 
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    firefox_options = Options()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--disable-gpu")
    firefox_driver = webdriver.Firefox(options=firefox_options)
    firefox_driver.get(webpage_url)

    scroll_height = firefox_driver.execute_script("return document.body.scrollHeight")
    prev_scroll_height = 0
    same_scroll_height_freq = 0 #How many times we see the same value for scroll height

    time.sleep(5)
    while same_scroll_height_freq < 10:
        firefox_driver.execute_script(f"window.scrollBy(0,{1000});")
        scroll_height = firefox_driver.execute_script("return document.body.scrollHeight")
        time.sleep(.05)  # Allow images to load
        if prev_scroll_height == scroll_height:
            same_scroll_height_freq += 1
        else:
            same_scroll_height_freq = 0
            prev_scroll_height = scroll_height 
 
    network_requests = firefox_driver.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")
    current_image_number = 0 

    for entry in network_requests:
        if 'initiatorType' in entry and entry['initiatorType'] == 'img':
            image_url = entry['name']
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(folder_path + "/"+ str(current_image_number) + '.png', 'wb') as file:
                    file.write(response.content)
                current_image_number += 1
            else:
                print(f'Failed to download {entry['name']}')

if __name__ == "__main__":
    FindImages("https://www.imdb.com/title/tt27714840/")