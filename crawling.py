import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Chrome 옵션 설정
chrome_options = Options()

# 웹드라이버 실행
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)
# 다운로드 경로 지정 (예: C:/my_download_folder)
# ※ Windows 환경이라면 역슬래시(\) 대신 슬래시(/) 또는 raw string(r"경로") 사용 권장
prefs = {
    "download.default_directory": r"C:\Users\youngjun\work\2025\datacrawling\dataset",  # 원하는 경로 지정
    "download.prompt_for_download": False,                   # 다운로드 시 대화창 표시 X
    "download.directory_upgrade": True                       # 기존 경로가 존재하지 않을 시 생성
}
chrome_options.add_experimental_option("prefs", prefs)

# 드라이버 실행
driver = webdriver.Chrome(options=chrome_options)

# 웹사이트 접속
url = "https://www.ftc.go.kr/www/selectBizCommOpenList.do?key=255"  # 실제 URL 사용
driver.get(url)
time.sleep(3)  # 페이지 로딩 대기

# 시/도 선택 드롭다운 (ID: searchInst1)
select_sido = Select(driver.find_element(By.ID, "searchInst1"))
sido_options = [option.get_attribute("value") for option in select_sido.options]

for sido_option in tqdm(sido_options[1:]):
    select_sido.select_by_value(sido_option)
    time.sleep(2)

    # 현재 선택된 시/도의 텍스트를 가져와 변수에 저장
    current_sido_text = select_sido.first_selected_option.text
    print(f"현재 선택된 시/도: {current_sido_text}")

    # 시/군/구 선택 드롭다운 (ID: searchInst2)
    select_sigungu = Select(driver.find_element(By.ID, "searchInst2"))
    sigungu_options = [option.get_attribute("value") for option in select_sigungu.options]

    # 시/군/구 선택
    select_sigungu.select_by_value(sigungu_options[0])
    time.sleep(2)
    
    # 다운로드 버튼 클릭
    download_button = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/form/fieldset/div/div/div/div[3]/a')
    download_button.click()
    print("✅ 다운로드 버튼 클릭 성공!")




# # 원하는 시/도 선택 (예: 서울특별시)
# select_sido.select_by_value("6110000")  # '서울특별시'의 value 값
# time.sleep(2)  # 변경된 데이터를 로딩할 시간 대기

# # 상세 지역구 선택 드롭다운 (ID: searchInst2)
# select_sigungu = Select(driver.find_element(By.ID, "searchInst2"))

# # 상세 지역 리스트 가져오기
# sigungu_options = [option.get_attribute("value") for option in select_sigungu.options]
# print(f"선택한 시/도의 상세 지역구 목록: {sigungu_options}")

# select_sigungu.select_by_value(sigungu_options[1])

# time.sleep(2)

# download_button = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/form/fieldset/div/div/div/div[3]/a')
# download_button.click()
# print("✅ 다운로드 버튼 클릭 성공!")

# # 예제: 첫 번째 상세 지역구 선택
# if len(sigungu_options) > 1:
#     select_sigungu.select_by_index(1)  # 첫 번째 지역 선택 (전체 제외)
#     time.sleep(2)

# # 여기서 추가적인 크롤링 로직 구현 가능

# 브라우저 종료
driver.quit()
