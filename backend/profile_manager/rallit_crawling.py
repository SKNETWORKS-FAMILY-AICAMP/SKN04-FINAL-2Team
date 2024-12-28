import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# 현재 스크립트의 절대 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# PDF와 이력서 저장 경로 설정
PDF_DIR = os.path.join(BASE_DIR, 'data', 'pdf')
RESUME_DIR = os.path.join(BASE_DIR, 'data', 'resume')

# 디렉토리 생성
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(RESUME_DIR, exist_ok=True)

def process_resume(i, j):
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--kiosk-printing')
    # chrome_options.add_argument('--headless')  # 브라우저 창 없이 실행
    # chrome_options.add_argument('--disable-dev-shm-usage')  # 메모리 사용 최적화

    chrome_prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps({
            'recentDestinations': [{'id': 'Save as PDF', 'origin': 'local', 'account': ''}],
            'selectedDestinationId': 'Save as PDF',
            'version': 2
        }),
        'savefile.default_directory': PDF_DIR,
        'download.default_directory': PDF_DIR,
        'savefile.prompt_for_download': False,
        'download.directory_upgrade': True,
        'download.prompt_for_download': False
    }
    chrome_options.add_experimental_option('prefs', chrome_prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(10)  # 페이지 로딩 타임아웃 설정
    
    try:
        url = f'https://www.rallit.com/hub?pageNumber={i}'
        driver.get(url)
        time.sleep(1)  # 대기 시간 감소

        driver.find_element(By.CSS_SELECTOR, f'section ul li:nth-child({j}) a article').click()
        time.sleep(1)  # 대기 시간 감소

        bs = BeautifulSoup(driver.page_source, 'lxml')
        resume = bs.select('div.css-1799hu')[0].text
        driver.execute_script('window.print();')
        time.sleep(2)

        # PDF 파일명 설정 및 이동
        pdf_filename = f"pdf_resume_{i:03d}_{j:02d}.pdf"
        pdf_path = os.path.join(PDF_DIR, pdf_filename)
        
        # 가장 최근 생성된 PDF 파일 찾기
        pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]
        if pdf_files:
            latest_file = max(pdf_files, key=lambda x: os.path.getctime(os.path.join(PDF_DIR, x)))
            os.rename(os.path.join(PDF_DIR, latest_file), pdf_path)

        # 텍스트 파일 저장
        resume_filename = f"resume_{i:03d}_{j:02d}.txt"
        resume_path = os.path.join(RESUME_DIR, resume_filename)
        with open(resume_path, "w", encoding="utf-8") as file:
            file.write(resume)
            
        print(f"처리 완료: {i}-{j}")
        
    except Exception as e:
        print(f"에러 발생 ({i}-{j}): {str(e)}")
    finally:
        driver.quit()

# 일반 반복문으로 실행
for i in range(1, 91):
    for j in range(1, 37):
        process_resume(i, j)