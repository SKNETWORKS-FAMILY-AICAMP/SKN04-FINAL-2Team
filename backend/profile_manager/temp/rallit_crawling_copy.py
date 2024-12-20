from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
from datetime import datetime
import time
from tqdm import tqdm

# 웹드라이버 설정 및 초기화 함수
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 브라우저를 보이지 않고 실행하는 옵션
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

# 이력서 텍스트를 가져오는 함수
def get_resume_text(driver, wait):
    try:
        content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-1799hu')))
        return content.text
    except TimeoutException:
        return None

# 이력서 크롤링 함수
def crawl_resumes(url):
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    
    # 저장할 폴더 생성
    folder = "resume_data"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    current_date = datetime.now().strftime("%Y%m%d")

    try:
        driver.get(url)
        count = 1
        while True:
            # 페이지의 이력서 항목들 크롤링
            for j in tqdm(range(1, 1)):
                count += 1
                try:
                    resume_xpath = f'/html/body/div[1]/main/section/div[4]/div/div[2]/section/ul/li[{j}]/a/article'
                    resume_element = wait.until(EC.element_to_be_clickable((By.XPATH, resume_xpath)))
                    resume_element.click()
                    
                    if text := get_resume_text(driver, wait):
                        # 이력서를 즉시 파일로 저장
                        filename = os.path.join(folder, f"resume_{current_date}_{j}.txt")
                        with open(filename, "w", encoding='utf-8') as file:
                            file.write(text)
                    
                    driver.back()
                    wait.until(EC.presence_of_element_located((By.XPATH, resume_xpath)))
                    
                except (TimeoutException, NoSuchElementException):
                    continue
            # 다음 페이지 버튼 처리
            next_button = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/main/section/div[4]/div/div[2]/section/div/div/button[7]")))
            
            if next_button.get_attribute("disabled") == 'true':
                break
                
            next_button.click()
            time.sleep(3)  # 페이지 전환 대기
            # 마지막 페이지 번호로 이동
            # https://www.rallit.com/hub?pageNumber=85 
    finally:
        driver.quit()

# 크롤링한 이력서를 파일로 저장하는 함수
# def save_resumes(resumes, filename="list.txt"):
#     with open(filename, "w", encoding='utf-8') as file:
#         for item in resumes:
#             file.write(item + "\n")

if __name__ == "__main__":
    url = "https://www.rallit.com/hub"
    resumes = crawl_resumes(url)
    # save_resumes(resumes)