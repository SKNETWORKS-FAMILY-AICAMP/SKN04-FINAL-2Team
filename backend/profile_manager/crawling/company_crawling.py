from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import os
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

company_name = []
establishment_year = []
company_scale = []
invest = []

company_name_example = ['유엔에스네트웍스', '커피팅', '더블유클럽', '인프랩', '서클플랫폼주식회사', '스타오토모빌', '이노그루']
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = 'https://thevc.kr/'
driver.get(url)
time.sleep(3)
driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/header/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div/input').click()
time.sleep(2)
send_key = driver.find_element(By.XPATH, '/html/body/div[3]/section/div[2]/form/div[1]/input')
send_key.send_keys('본인 아이디 입력') #아이디 입력
send_key = driver.find_element(By.XPATH, '/html/body/div[3]/section/div[2]/form/div[2]/input')
send_key.send_keys('본인 비밀번호 입력') #비밀번호 입력
driver.find_element(By.XPATH, '/html/body/div[3]/section/div[2]/form/button[2]/div[2]').click()
time.sleep(5)

for i in company_name_example:    
    try:
        driver.get(url)
        time.sleep(5)
        send_key = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/header/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div/input')
        send_key.send_keys(i)
        send_key.send_keys(Keys.RETURN)
        time.sleep(5)
        if '기업 검색 결과' in driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[1]/div[1]/div/h2').text:
            driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[1]/div[1]/ul/li/div').click()
        time.sleep(5)
        company_name.append(driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/p[1]/span[2]/mark').text)
        establishment_year.append(driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/p[1]/span[4]/mark').text)
        company_scale.append(driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/p[1]/span[6]/mark').text)
        # if 'Seed' in driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[2]').text or 'Series' in driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[2]').text or 'M&A' in driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[2]').text:
        #     invest.append(driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[2]').text)
        # else:
        #     invest.append('None')
        if '현재 라운드' in driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]').text:
            invest.append(driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[2]').text)
        else:
            invest.append('None')
    except NoSuchElementException:
        continue
    except Exception:
        continue
    except IndexError:
        continue


