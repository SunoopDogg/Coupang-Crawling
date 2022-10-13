import os
import shutil
import subprocess
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def init_craw():    # {
    try:
        shutil.rmtree(r"c:\chrometemp")  # 쿠키 / 캐쉬파일 삭제
    except FileNotFoundError:
        pass

    subprocess.Popen(
        r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  # 디버거 크롬 구동
# }


def get_path():  # {
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'

    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)

    return driver_path
# }


def get_driver(driver_path):    # {
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_options.add_argument('headless')
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument(
        "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")
    chrome_options.add_argument("lang=ko_KR")

    driver = webdriver.Chrome(driver_path, options=chrome_options)
    driver.set_window_position(0, 0)
    driver.set_window_size(1920, 1080)
    return driver
# }
