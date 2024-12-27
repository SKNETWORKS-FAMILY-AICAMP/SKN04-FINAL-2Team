from bs4 import BeautifulSoup
from tqdm import tqdm

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from tqdm import tqdm

url = "https://www.rallit.com/hub"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)

resume = []
while True:
    for j in tqdm(range(1, 37)):
        try:
            driver.find_element(By.XPATH, f'/html/body/div[1]/main/section/div[4]/div/div[2]/section/ul/li[{j}]/a/article').click()
            time.sleep(4)
            bs = BeautifulSoup(driver.page_source, 'lxml')
            resume.append(bs.select('div.css-1799hu')[0].text)
            time.sleep(5)
            driver.back()
            time.sleep(9)

        except NoSuchElementException:
            driver.back()
            continue
        except Exception:
            driver.back()
            continue
        except IndexError:
            driver.back()
            continue

    button = driver.find_element(By.XPATH, "/html/body/div[1]/main/section/div[4]/div/div[2]/section/div/div/button[7]")  # 버튼의 ID 사용
    if button.get_attribute("disabled") != 'true':
        button.click()
        time.sleep(10)
    else:
        break

with open("list.txt", "w") as file:
    for item in resume:
        file.write(item + "\n")
