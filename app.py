from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import csv
from parsel import Selector
from selenium.webdriver.common.by import By
from time import sleep
import pytesseract
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import *
import parameter
import random
ser =Service('chromedriver.exe')
# ua = UserAgent()
# userAgent = ua.random
# proxies = ['49.12.43.32:443','183.82.99.126:3128','1.186.82.4:5678','203.115.123.165:9999','103.206.51.225:83']
# PROXY = random.choice(proxies)
PROXY = '103.69.45.87:58199	'
webdriver.DesiredCapabilities.CHROME['proxy'] = {
"httpProxy": PROXY,
"ftpProxy": PROXY,
"sslProxy": PROXY,
"proxyAutoconfigUrl": '',
"noProxy": '',
"proxyType": "MANUAL",
"class": "org.openqa.selenium.Proxy",
"autodetect": False
}


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
if os.path.isfile(parameter.folder):
    os.remove(parameter.folder)
# chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166')
driver = webdriver.Chrome(service=ser,options=chrome_options,)
driver.get('https://www.linkedin.com/login')
driver.maximize_window()
sleep(0.5)
user_name = driver.find_element(By.XPATH,'//input[@id="username"]').send_keys(parameter.user_name)
password = driver.find_element(By.XPATH,'//input[@id="password"]').send_keys(parameter.pwd)
sleep(0.5)
driver.find_element(By.XPATH,'//button[@type="submit"]').click()
sleep(1)
driver.get('https://www.google.com/')
sleep(1)
search = driver.find_element(By.XPATH, '//input[@class="gLFyf gsfi"]')
sleep(1)
search.send_keys(parameter.g_search)

# search.send_keys(Keys.RETURN)
driver.find_element(By.XPATH,'//div[@class="FPdoLc lJ9FBc"]//input[@class="gNO89b"]').click()
sleep(20)
page_count =5
dev_list = []
def start():
    global page_count
    while page_count>1:
        sel1 = Selector(text=driver.page_source)
        profiles = sel1.xpath('//div[@class="yuRUbf"]/a/@href').extract()
        dev_list.append(profiles)
        driver.find_element(By.ID,"pnnext").click()
        page_count -= 1
        start()

    return 'Done'

start()
with open(parameter.folder,'w') as myfile:
    writer = csv.writer(myfile,delimiter=",",lineterminator='\r')
    for li in dev_list:
        for i in li:
            try:
                driver.get(i)
                sleep(0.5)
                driver.find_element(By.XPATH,'//div[@class="pv-top-card-v2-ctas pt2 display-flex"]/div/button').click()
                sleep(0.5)
                driver.find_element(By.XPATH,'//span[@class="display-flex t-normal"]').click()
                sleep(0.5)
                driver.find_element(By.XPATH,'//button[@aria-label="Connect"]').click()
                sleep(2)
            except NoSuchElementException as e:
                writer.writerow([i])
                print(e)
                continue
    myfile.close()

driver.quit()