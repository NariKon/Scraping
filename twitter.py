#!/usr/local/bin/python3 227.py

import os
from time import sleep


def get_res(links):
    import requests
    
    url = 'https://twitter.com/'
    response = []
        
    for link in links:
        res = requests.get(url+link)
        res.raise_for_status()

        response.append(res)

    return response


def evaluate_link(link):
    if link == None:
        return False
    elif link.startswith('https://pbs.twimg.com/media/'):
        return True
    else:
        return False
    
    return False


def get_img_links(res):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(res.text, "html.parser")
    imgs = soup.select('img')

    links = []
    for img in imgs:
        link = img.get('src')

        if evaluate_link(link):
            links.append(link)
            print(link)
        else:
            continue

    
    print(len(links), 'imgs')

    return links


def get_all_page(link):
    from selenium import webdriver

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',
                              options=options)
    driver.get('https://twitter.com/'+link)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        # DELETE
        # break
        

    imgs = driver.find_elements_by_css_selector('img')
    
    links = []
    for img in imgs:
        link = img.get_attribute('src')
        if evaluate_link(link):
            link = link.replace(':thumb', '')
            links.append(link)            
        
    driver.quit()
    
    print(len(links), 'imgs')
    return links

    
def stop():
    import sys
    sys.exit()

    
if __name__ == '__main__':
    from urllib.request import urlretrieve
    import pprint
    import sys
    
    os.chdir(os.environ['HOME']+'/Documents')
    os.makedirs('Twitter', exist_ok=True)
    os.chdir('Twitter')

    girls = []
    if len(sys.argv) > 1:
        girls = sys.argv[1:]
    else:
        girls = ['sally_amaki',
                 'ru_ri_88',
                 'hanakawamei_227',
                 'reinyan_0526',
                 'c_hokaze227']

    last_record = {}
    
    # res = get_res(girls)
    # for girl, response in zip(girls, res):
    for girl in girls:
        print(girl, end='\t')
        os.makedirs(girl, exist_ok=True)
        os.chdir(girl)

        # links = get_img_links(response)
        links = get_all_page(girl)

        count = 0
        for link in links:
            urlretrieve(link, '{}-{}.jpg'.format(girl, count))
            count += 1

        os.chdir('../')

        last_record[girl] = links[0:4]

    with open('record.py',"w") as f:
        f.write('record='+pprint.pformat(last_record))
