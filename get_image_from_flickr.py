import os
import time
import sys
import logging
import threading

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logging.basicConfig(format='%(asctime)s>%(message)s', datefmt="%H:%M:%S", level=logging.INFO)
options = webdriver.ChromeOptions()
options.add_argument('--headless')


def get_list():
    url = 'https://flickr.com/search/?text='
    text = sys.argv[1]#input('Type search word: ')
    limit_str = sys.argv[2]#input('Type limit: ')
    limit = int(limit_str)

    os.makedirs(text, exist_ok=True)
    os.chdir(text)

    #TODO: change path name of executable_path
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
    driver.get(url+text)

    count = 20
    last_height = driver.execute_script('return document.body.scrollHeight;')
    while count < limit:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(3)
        new_height = driver.execute_script('return document.body.scrollHeight;')
        if last_height == new_height:
            logging.info('we have reached the limit of page')
            break

        count += 20

    elements = driver.find_elements_by_css_selector('div.photo-list-photo-interaction > a')
    hrefs = [element.get_attribute('href') for element in elements]

    driver.quit()

    return hrefs


def get_one_image(index, link):
    #TODO: change path name of executable_path
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
    driver.get(link)
    logging.info(link)
    time.sleep(2)

    imgs = driver.find_elements_by_css_selector('img')#WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.zoom-modal > div.zoom-photo-container > img")))
    src_list = [img.get_attribute('src') for img in imgs  if img.get_attribute('src').startswith('https://live.staticflickr.com')]

    with open("{}.jpg".format(index), "wb") as f:
        res = requests.get(src_list[1])
        for chunk in res.iter_content(1000000):
            f.write(chunk)


hrefs = get_list()
print(len(hrefs))
threads = list()
for i, href in enumerate(hrefs):
    x = threading.Thread(target=get_one_image, args=(i, href,))
    threads.append(x)
    x.start()

    while threading.activeCount() >= 5:
        time.sleep(1)