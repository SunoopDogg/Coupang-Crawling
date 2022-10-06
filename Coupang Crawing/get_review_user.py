import time
from init_craw import *
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

init_craw()
driver = get_driver(get_path())

url = 'https://www.coupang.com/vp/products/6135671335?itemId=11731447959&vendorItemId=80581549821&q=%EC%97%90%EC%96%B4%ED%8C%9F&itemsCount=30&searchId=68aae7e922f2401d90935d986eed9d0f&rank=0&isAddedCart='
driver.get(url)
driver.implicitly_wait(10)
time.sleep(1)

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


print(len(review_user_list))
driver.quit()
