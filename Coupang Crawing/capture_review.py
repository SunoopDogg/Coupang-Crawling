import time
from init_craw import *
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

product_id = input("product_id: ")
user_id = input("user_id: ")

init_craw()
driver = get_driver(get_path())

url = 'https://www.coupang.com/vp/products/'+product_id+'?'
driver.get(url)
driver.implicitly_wait(10)
time.sleep(1)

# 리뷰 탭 클릭
wait = WebDriverWait(driver, 5)
wait.until(EC.element_to_be_clickable((By.NAME, 'review'))).click()
driver.implicitly_wait(10)
time.sleep(1)

# Q&A 탭 클릭
wait.until(EC.element_to_be_clickable((By.NAME, 'qna'))).click()
driver.implicitly_wait(10)
time.sleep(0.5)

# 맨 위로 스크롤
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(0.5)

# 리뷰 페이지 소스 가져오기
soup = BeautifulSoup(driver.page_source, 'html.parser')


reviews = soup.select('article.sdp-review__article__list')  # 리뷰 리스트
review_user_id_list = [review.select_one('span.sdp-review__article__list__info__user__name')[
    'data-member-id'] for review in reviews]  # 리뷰 작성자 ID

# 리뷰 작성자 ID가 일치하는 리뷰의 인덱스
if (user_id in review_user_id_list):  # {
    index = review_user_id_list.index(user_id)

    # 리뷰 캡쳐
    element = driver.find_elements(
        By.CLASS_NAME, 'sdp-review__article__list')[index]
    element_png = element.screenshot_as_png
    with open('captures\\'+user_id+'_'+product_id+'.png', 'wb') as file:
        file.write(element_png)
# }
