import datetime
import os
import time
import shutil
import subprocess
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    shutil.rmtree(r"c:\chrometemp")  # 쿠키 / 캐쉬파일 삭제
except FileNotFoundError:
    pass

subprocess.Popen(
    r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  # 디버거 크롬 구동


option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument(
    "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")
options.add_argument("lang=ko_KR")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
driver_path = f'./{chrome_ver}/chromedriver.exe'

if os.path.exists(driver_path):
    print(f"chrom driver is insatlled: {driver_path}")
else:
    print(f"install the chrome driver(ver: {chrome_ver})")
    chromedriver_autoinstaller.install(True)

driver = webdriver.Chrome(driver_path, options=option)

url = 'https://www.coupang.com/vp/products/6135671335?itemId=11731447959&vendorItemId=80581549821&q=%EC%97%90%EC%96%B4%ED%8C%9F&itemsCount=30&searchId=68aae7e922f2401d90935d986eed9d0f&rank=0&isAddedCart='
driver.get(url)
driver.implicitly_wait(10)
time.sleep(1)
# for i in range(1, 10000, 5):
#     driver.execute_script("window.scrollTo(0, {})".format(i))
wait = WebDriverWait(driver, 5)
wait.until(EC.element_to_be_clickable((By.NAME, 'review'))).click()
driver.implicitly_wait(10)
time.sleep(1)

review_user_list = []
index = 1
while True:
    wait.until(EC.element_to_be_clickable((By.NAME, 'qna'))).click()
    driver.implicitly_wait(10)
    time.sleep(0.5)

    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(0.5)

    review_page_button = driver.find_elements(
        By.XPATH, '//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/div[3]/button')
    if (index == 12):
        index = 2

    review_page_button[index % 12].click()
    index += 1
    driver.implicitly_wait(10)
    time.sleep(0.5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    review_user_list.append(soup.select(
        'div.sdp-review__article__list__info__user'))

    # review_users = [
    #     review_user.text for review_user in review_user_list]


print(len(review_user_list))
time.sleep(10)
driver.quit()
