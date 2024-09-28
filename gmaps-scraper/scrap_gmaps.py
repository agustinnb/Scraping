from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time
import json
import os

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--ignore-certificate-errors-spki-list')
driver = webdriver.Chrome(chrome_options=options)
url = r'https://www.google.com/maps/search/pickleball+courts+Abbott+Park/@48.4829879,-125.9076358,6z'
driver.get(url)
time.sleep(5)
page_content=driver.page_source

elements= driver.find_elements(By.XPATH,'//div[contains(@aria-label, "Resultados de")]/div')
i=0

try:
    while (elements[i] is not None):
        driver.execute_script('arguments[0].scrollIntoView(true);', elements[i])
        elements= driver.find_elements(By.XPATH,'//div[contains(@aria-label, "Resultados de")]/div')
        i=i+1
        time.sleep(1)    
except IndexError:
    pass
print('Termine')
#for i in range(0,len(elements)):
#    driver.execute_script('arguments[0].scrollIntoView(true);', elements[i])
#    time.sleep(2)    




