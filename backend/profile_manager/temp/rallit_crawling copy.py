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

    try:
        driver.get(url)
        # 테스트용으로 1페이지만 크롤링 (95 페이지 까지 가능)
        for page in tqdm(range(1, 2)):
            # 페이지의 이력서 항목들 크롤링
            for item in tqdm(range(1, 37)):
                try:
                    resume_xpath = f'/html/body/div[1]/main/section/div[4]/div/div[2]/section/ul/li[{item}]/a/article'
                    resume_element = wait.until(EC.element_to_be_clickable((By.XPATH, resume_xpath)))
                    
                    # 파일이 이미 존재하는지 확인
                    filename = os.path.join(folder, f"resume_{page:03d}_{item:02d}.txt")
                    if os.path.exists(filename):
                        continue
                        
                    resume_element.click()
                    
                    if text := get_resume_text(driver, wait):
                        # 이력서를 즉시 파일로 저장
                        with open(filename, "w", encoding='utf-8') as file:
                            file.write(text)
                    
                    driver.back()
                    wait.until(EC.presence_of_element_located((By.XPATH, resume_xpath)))
                    
                except (TimeoutException, NoSuchElementException):
                    continue
            # 다음 페이지로 이동
                
            next_url = f"https://www.rallit.com/hub?pageNumber={page}"
            driver.get(next_url)
            time.sleep(3)  # 페이지 로딩 대기
    finally:
        driver.quit()

if __name__ == "__main__":
    url = "https://www.rallit.com/hub"
    resumes = crawl_resumes(url)