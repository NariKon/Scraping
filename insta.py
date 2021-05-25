import os
import time
import threading
import logging

from selenium import webdriver
from urllib.request import urlretrieve

post_selector = "div.v1Nh3.kIKUG._bz0w > a"
text_selector = "h2._6lAjh + span"
image_selector = "div.KL4Bh > img"
time_selecotr = "a.c-Yi7 > time"

options = webdriver.ChromeOptions()
options.add_argument('--headless')

threads = list()
logging.basicConfig(format="%(asctime)s>%(message)s", datefmt="%H:%M:%S", level=logging.INFO)


def get_all_post_link(url):
	driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=options)
	driver.get(url)

	links = list()
	now_height = driver.execute_script("return document.body.scrollHeight")
	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(2)
		new_height = driver.execute_script("return document.body.scrollHeight")
		if now_height < new_height:
			now_height = new_height
		else:
			break

		elements = driver.find_elements_by_css_selector(post_selector)
	

		for element in elements:
			href = element.get_attribute('href')
			if not href in links:
				links.append(href)

	return links


def get_one_post(link):
	logging.info("%s", link)
	driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=options)
	driver.get(link)
	texts = driver.find_elements_by_css_selector(text_selector)
	imgs = driver.find_elements_by_css_selector(image_selector)
	date = driver.find_elements_by_css_selector(time_selecotr)
	
	text = ''
	date_str = ''
	date_code = ''

	if(len(date)):
		date_str = date[0].get_attribute("title")
		date_code = date[0].get_attribute("datetime")
		if date_code[:-14]+'.txt' in os.listdir():
			logging.info("Skipped (%s)", date_code)
			driver.quit()
			return

	if(len(texts)):
		text = texts[0].text
		with open(date_code[:-14]+'.txt', "w") as f:
			f.write(text+'\n'+date_str)

	if(len(imgs)):
		for index, img in enumerate(imgs):
			urlretrieve(img.get_attribute("src"), date_code[:-14]+'_'+str(index+1)+'.jpg')

	driver.quit()

def format_folder():
	for file in os.listdir():
		os.makedirs(file[:5], exist_ok=True)

	for obj in os.scandir():
		if  obj.is_dir():
			continue
		os.rename(obj.name, obj.name[5:])
	
	for obj in os.scandir():
		if  obj.is_dir():
			continue
		os.rename(obj.name, obj.name[:5]+'/'+obj.name)
		

if __name__ == "__main__":
	base_url = "https://instagram.com/"
	person_id = input("person_id >>> ") #"sallyamaki"

	os.chdir('/Users/narikon/ImageSet')
	os.makedirs(person_id, exist_ok=True)
	os.chdir(person_id)

	links = get_all_post_link(base_url+person_id)
	logging.info("Got all links, now loading...")

	for link in links:
		x = threading.Thread(target=get_one_post, args=(link,))
		threads.append(x)
		x.start()

		time.sleep(1)

		while threading.activeCount() > 10:
			time.sleep(2)

	for thread in threads:
		thread.join()