import pandas as pd  # pandas 라이브러리 임포트
import requests  # 웹 페이지를 가져올 때 사용할 requests 라이브러리 임포트
from bs4 import BeautifulSoup  # 웹 페이지의 HTML을 파싱할 때 사용할 BeautifulSoup 라이브러리 임포트
from tqdm import tqdm  # 작업 진행 상태를 표시할 tqdm 라이브러리 임포트

import time  # 시간 관련 기능을 제공하는 time 라이브러리 임포트
from selenium import webdriver  # 웹 브라우저를 자동화할 때 사용할 selenium 라이브러리 임포트
from selenium.webdriver.chrome.service import Service  # 크롬 브라우저 서비스를 관리하는 Service 클래스 임포트
from webdriver_manager.chrome import ChromeDriverManager  # 크롬 브라우저 드라이버를 관리하는 ChromeDriverManager 클래스 임포트
from selenium.webdriver.common.by import By  # 웹 페이지의 요소를 찾을 때 사용할 By 클래스 임포트
from selenium.webdriver.support.ui import WebDriverWait  # 웹 페이지의 요소가 로드될 때까지 기다리는 WebDriverWait 클래스 임포트
from selenium.webdriver.support import expected_conditions as EC  # 웹 페이지의 요소가 로드될 때까지 기다리는 조건을 정의하는 expected_conditions 클래스 임포트
from selenium.webdriver.common.keys import Keys  # 웹 페이지에서 키보 입력을 시뮬레이션하는 Keys 클래스 임포트
from selenium.common.exceptions import NoSuchElementException  # 웹 페이지에서 요소를 찾지 못하는 예외를 처리하는 NoSuchElementException 클래스 임포트

url = "https://www.rallit.com/"  # 크롤링할 웹 페이지의 URL
response = requests.get(url, headers={'User-Agent': 'Mozilla 5.0'})  # 웹 페이지를 가져올 때 사용자 에이전트를 설정
bs = BeautifulSoup(response.text, 'lxml')  # 웹 페이지의 HTML을 BeautifulSoup으로 파싱
languages = bs.select('div.css-1ady226 a')  # 웹 페이지에서 특정 클래스를 가진 링크를 모두 선택
urls = ''.join([url,languages[2].attrs.get('href').split('/')[1]])  # 선택한 링크 중 하나의 URL을 완성
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))  # 크롬 브라우저 드라이버를 설치하고 브라우저를 시작
driver.get(urls)  # 완성된 URL로 브라우저를 이동

Resume = []  # 이력서 텍스트를 저장할 리스트
for i in range(1, 37):  # 1부터 36까지 반복
    try:
        driver.find_element(By.XPATH, f'/html/body/div[1]/main/section/div[4]/div/div[2]/section/ul/li[{i}]/a/article').click()  # 웹 페이지의 특정 요소를 클릭
        time.sleep(4)  # 클릭 후 4초간 대기
        bs = BeautifulSoup(driver.page_source, 'lxml')  # 브라우저의 현재 페이지 소스를 BeautifulSoup으로 파싱
        Resume.append(bs.select('div.css-1799hu')[0].text)  # 파싱한 HTML에서 특정 클래스를 가진 요소의 텍스트를 이력서 리스트에 추가
        time.sleep(5)  # 이력서 텍스트를 추가한 후 5초간 대기
        driver.get(urls)  # 원래 URL로 브라우저를 이동
        time.sleep(9)  # 브라우저를 이동한 후 9초간 대기

    except NoSuchElementException:  # 웹 페이지에서 요소를 찾지 못하는 예외가 발생하면
        driver.get(urls)  # 원래 URL로 브라우저를 이동
        continue  # 다음 반복으로 이동
    except Exception as e:  # 다른 예외가 발생하면
        driver.get(urls)  # 원래 URL로 브라우저를 이동
        continue  # 다음 반복으로 이동
    except IndexError:  # 인덱스 오류가 발생하면
        driver.get(urls)  # 원래 URL로 브라우저를 이동
        continue  # 다음 반복으로 이동