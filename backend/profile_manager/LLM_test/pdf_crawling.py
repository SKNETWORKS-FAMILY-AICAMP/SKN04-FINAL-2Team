from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import os
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# PDF 저장 경로
pdf_save_path = r'C:\Users\USER\Documents\final_project\SKN04-FINAL-2Team\SKN04-FINAL-2Team\backend\profile_manager\LLM_test\pdf'

# 경로가 존재하지 않으면 생성
if not os.path.exists(pdf_save_path):
    os.makedirs(pdf_save_path)


for i in range(1, 91):
    for j in range(1, 37):
        # Chrome 옵션 설정
        chrome_options = Options()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--kiosk-printing')  # 인쇄 대화상자 생략

        # PDF 저장을 위한 프린트 설정
        chrome_prefs = {
            'printing.print_preview_sticky_settings.appState': json.dumps({
                'recentDestinations': [{'id': 'Save as PDF', 'origin': 'local', 'account': ''}],
                'selectedDestinationId': 'Save as PDF',
                'version': 2
            }),
            'savefile.default_directory': pdf_save_path,  # PDF 저장 경로
            'download.default_directory': pdf_save_path,  # 다운로드 경로 설정
            'savefile.prompt_for_download': False,  # 다운로드 창 비활성화
            'download.directory_upgrade': True,  # 디렉토리 업그레이드 허용
            'download.prompt_for_download': False  # 다운로드 대화상자 비활성화
        }
        chrome_options.add_experimental_option('prefs', chrome_prefs)

        driver = webdriver.Chrome(options=chrome_options)
        try:
            url = f'https://www.rallit.com/hub?pageNumber={i}'  # 원하는 URL 입력
            driver.get(url)
            time.sleep(5)

            driver.find_element(By.XPATH, f'/html/body/div[1]/main/section/div[4]/div/div[2]/section/ul/li[{j}]/a/article').click()

            # 페이지 로딩 대기
            time.sleep(5)
            bs = BeautifulSoup(driver.page_source, 'lxml')
            resume = bs.select('div.css-1799hu')[0].text
            driver.execute_script('window.print();')
            time.sleep(5)  # PDF 저장 대기

            # 최신 파일 이름 확인 및 변경
            files = os.listdir(pdf_save_path)
            files = [os.path.join(pdf_save_path, f) for f in files if f.endswith('.pdf')]
            latest_file = max(files, key=os.path.getctime)  # 가장 최근에 생성된 파일 찾기

            custom_filename = os.path.join(pdf_save_path, f"pdf_resume_{i:03d}_{j:02d}.pdf")
            os.rename(latest_file, custom_filename)
            print(f"PDF 저장 완료! 저장 경로: {pdf_save_path}")

            with open(f"resume/resume_{i:03d}_{j:02d}.txt", "w", encoding="utf-8") as file:
                file.write(resume)
        except NoSuchElementException as e:
            continue
        except IndexError as e:
            continue
        except Exception as e:
            continue
        finally:
            driver.quit()
