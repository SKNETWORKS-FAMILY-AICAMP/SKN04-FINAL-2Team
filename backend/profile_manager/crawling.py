import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

url = "https://www.rallit.com/"
response = requests.get(url, headers={'User-Agent': 'Mozilla 5.0'})
bs = BeautifulSoup(response.text, 'lxml')
languages = bs.select('div.css-1ady226 a')
urls = ''.join([url,languages[2].attrs.get('href').split('/')[1]])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(urls)

Resume = []
for i in range(1, 37):
    try:
        driver.find_element(By.XPATH, f'/html/body/div[1]/main/section/div[4]/div/div[2]/section/ul/li[{i}]/a/article').click()
        time.sleep(4)
        bs = BeautifulSoup(driver.page_source, 'lxml')
        Resume.append(bs.select('div.css-1799hu')[0].text)
        time.sleep(5)
        driver.get(urls)
        time.sleep(9)

    except NoSuchElementException:
        driver.get(urls)
        continue
    except Exception as e:
        driver.get(urls)
        continue
    except IndexError:
        driver.get(urls)
        continue
    