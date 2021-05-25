import os
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

# import ranking

def cd_to_python_dir():
    os.chdir('/Users/narikon/Desktop/Code/Python')
    os.makedirs('src', exist_ok=True)
    os.chdir('src')

def get_word_and_limit(limit=10):
    print('Words: ', end='')
    words = input()

    while(1):
        print('Limit: ', end='')
        limit_str = input()
        try:
            limit = int(limit_str)
            break
        except:
            print('This is not number...')

    os.makedirs(words, exist_ok=True)
    os.chdir(words)
    
    return (words, limit)


def get_images(words, driver, image_driver, limit):
    url = 'https://www.bing.com/images/search?q={}'.format(words.replace(' ', '+'))
    driver.get(url)

    load_units = 35

    last_height = driver.execute_script("return document.body.scrollHeight")
    while (limit - load_units > 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if load_units > limit:
            break
        last_height = new_height
        load_units += 35


    a_tags = driver.find_elements_by_css_selector('div#b_content > div#vm_c > div.dg_b > div > ul > li > div > div > a')

    for index, a_tag in enumerate(a_tags):
        if index == limit:
            break
    
        href_url = a_tag.get_attribute('href')
        img_driver.get(href_url)

        while(1):
            try:
                src_url = img_driver.find_element_by_css_selector('#b_content > #detailPage > #detailCanvas > #mainImageRegion > #mainImageContainer > #mainImageViewer > #mainImageWindow > div.mainImage.current > div > div > div > img').get_attribute('src')
                break
            except:
                img_driver.implicitly_wait(2)

            
        if len(src_url) == 0:
            print('no result')
            break

        print(src_url)
            
        file_name = '{}_{}.jpg'.format(words.replace(' ', '-'), index+1)
        try:
            urlretrieve(src_url, file_name)
        except:
            continue
        # src_res = requests.get(src_url)

        # with open('{}_{}.jpg'.format(words.replace(' ', '-'), index+1), "wb") as f:
        #    for chunk in src_res.iter_content(1000000):
        #        f.write(chunk)



if __name__ == '__main__':
    cd_to_python_dir()
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
    img_driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)

    
    words, limit = get_word_and_limit()
    get_images(words, driver, img_driver, limit)
    # limit=5
    # name_list = []
    # for name in ranking.ranking['1']:
    #     if name in name_list:
    #         continue

    #     print("Downloading:", name)
        
        
     #    get_images(name, driver, img_driver, limit)

     #    name_list.append(name)
    
    driver.quit()
    img_driver.quit()
