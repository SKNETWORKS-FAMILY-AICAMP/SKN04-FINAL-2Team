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
import json
import glob
import shutil
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

def setup_chrome_for_pdf(pdf_folder):
    """PDF 저장을 위한 Chrome 설정"""
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--kiosk-printing')

    chrome_prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps({
            'recentDestinations': [{'id': 'Save as PDF', 'origin': 'local', 'account': ''}],
            'selectedDestinationId': 'Save as PDF',
            'version': 2
        }),
        'savefile.default_directory': pdf_folder,
        'download.default_directory': pdf_folder,
        'savefile.prompt_for_download': False,
        'download.directory_upgrade': True,
        'download.prompt_for_download': False
    }
    
    chrome_options.add_experimental_option('prefs', chrome_prefs)
    service = Service(ChromeDriverManager().install())
    return chrome_options, service

def rename_latest_pdf(new_filename):
    pdf_folder = os.path.abspath("resume_pdf")
    try:
        # 가장 최근에 다운로드된 PDF 파일 찾기
        list_of_files = glob.glob(os.path.join(pdf_folder, '*.pdf'))
        latest_file = max(list_of_files, key=os.path.getctime)
        
        # 새로운 경로로 이동/이름변경
        new_path = os.path.join(pdf_folder, f"{new_filename}.pdf")
        shutil.move(latest_file, new_path)
        return True
    except Exception as e:
        print(f"파일 이름 변경 실패: {str(e)}")
        return False

def move_pdf_from_temp(temp_dir, pdf_folder, new_filename):
    try:
        # 임시 폴더에서 PDF 찾기
        pdf_files = [f for f in os.listdir(temp_dir) if f.endswith('.pdf')]
        if not pdf_files:
            print("임시 폴더에서 PDF를 찾을 수 없습니다.")
            return False
            
        # 임시 폴더의 PDF 파일 이동 (첫 번째 PDF 파일 사용)
        temp_pdf = pdf_files[0]
        src_path = os.path.join(temp_dir, temp_pdf)
        dst_path = os.path.join(pdf_folder, f"{new_filename}.pdf")
        
        shutil.move(src_path, dst_path)
        print(f"PDF 이동 완료: {dst_path}")
        return True
        
    except Exception as e:
        print(f"PDF 이동 실패: {str(e)}")
        return False

def crawl_resumes(url):
    # 저장할 폴더 생성
    text_folder = "resume_data"
    pdf_folder = os.path.abspath("temp")
    for folder in [text_folder, pdf_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    chrome_options, service = setup_chrome_for_pdf(pdf_folder)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    try:
        driver.get(url)
        # 테스트용으로 1페이지만 크롤링 (95 페이지 까지 가능)
        for page in tqdm(range(1, 2)):
            # 페이지의 이력서 항목들 크롤링
            for item in tqdm(range(1, 4)):
                try:
                    resume_xpath = f'/html/body/div[1]/main/section/div[4]/div/div[2]/section/ul/li[{item}]/a/article'
                    resume_element = wait.until(EC.element_to_be_clickable((By.XPATH, resume_xpath)))
                    
                    base_filename = f"resume_{page:03d}_{item:02d}"
                    text_filename = os.path.join(text_folder, f"{base_filename}.txt")
                    
                    if os.path.exists(text_filename):
                        continue
                        
                    resume_element.click()
                    time.sleep(3)
                    
                    # BeautifulSoup을 사용하여 텍스트 추출
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    if content := soup.select_one('div.css-1799hu'):
                        # 텍스트 파일로 저장
                        with open(text_filename, "w", encoding='utf-8') as file:
                            file.write(content.text)
                        
                        # 최근 저장된 PDF 파일의 이름 변경
                        if rename_latest_pdf(pdf_folder, base_filename):
                            print(f"PDF 저장 완료: {base_filename}.pdf")
                        else:
                            print(f"PDF 이름 변경 실패: {base_filename}.pdf")
                    
                    driver.back()
                    wait.until(EC.presence_of_element_located((By.XPATH, resume_xpath)))
                    
                except Exception as e:
                    print(f"에러 발생: {str(e)}")
                    continue
                
            next_url = f"https://www.rallit.com/hub?pageNumber={page}"
            driver.get(next_url)
            time.sleep(3)
    finally:
        driver.quit()

if __name__ == "__main__":
    url = "https://www.rallit.com/hub"
    resumes = crawl_resumes(url)