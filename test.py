from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import shutil
import os

import requests


try:
    shutil.rmtree(r"c:\chrometemp")  # 쿠키 / 캐쉬파일 삭제
except FileNotFoundError:
    pass

subprocess.Popen(
    r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  # 디버거 크롬 구동


option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
driver_path = f'./{chrome_ver}/chromedriver.exe'

if os.path.exists(driver_path):
    print(f"chrom driver is insatlled: {driver_path}")
else:
    print(f"install the chrome driver(ver: {chrome_ver})")
    chromedriver_autoinstaller.install(True)

driver = webdriver.Chrome(driver_path, options=option)

driver.get("https://google.com")
driver.implicitly_wait(10)

url = 'https://www.coupang.com/np/search?q=%EC%95%84%EC%9D%B4%ED%8F%B0&channel=recent'
driver.get(url)
driver.implicitly_wait(10)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
res = requests.get(url, headers=headers)
print(res.text)

driver.quit()
