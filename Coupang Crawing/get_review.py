import time
import pandas as pd
from init_craw import *
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 쿠팡 상품 ID 입력
product_id = input("product_id: ")

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

review_user_name = []
review_user_id = []
review_user_date = []
review_user_star = []
review_user_content = []

index = 1
while True:  # {
    # Q&A 탭 클릭
    wait.until(EC.element_to_be_clickable((By.NAME, 'qna'))).click()
    driver.implicitly_wait(10)
    time.sleep(0.5)

    # 맨 위로 스크롤
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(0.5)

    # 리뷰 페이지 소스 가져오기
    review_page_button = driver.find_elements(
        By.XPATH, '//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/div[3]/button')

    if (index % 12 == 0):
        index += 2

    if (index == 20):
        break

    if (len(review_page_button) == 0):
        break
    print('index=', index)
    print('index%12=', index % 12)
    review_page_button[index % 12].click()
    driver.implicitly_wait(10)
    time.sleep(0.5)
    index += 1

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    reviews = soup.select('article.sdp-review__article__list')  # 리뷰 리스트
    review_user_name_list = [review.select_one(
        'span.sdp-review__article__list__info__user__name').get_text() for review in reviews]  # 리뷰 작성자 이름
    review_user_id_list = [review.select_one('span.sdp-review__article__list__info__user__name')[
        'data-member-id'] for review in reviews]    # 리뷰 작성자 ID
    review_user_date_list = [review.select_one(
        'div.sdp-review__article__list__info__product-info__reg-date').get_text() for review in reviews]  # 리뷰 작성일
    review_user_star_list = [review.select_one('div.sdp-review__article__list__info__product-info__star-orange')[
        'data-rating'] for review in reviews]  # 리뷰 별점
    # review_user_content_list = [review.select_one(
    #     'sdp-review__article__list__review__content').get_text() for review in review_list]  # 리뷰 내용

    review_user_name.extend(review_user_name_list)
    review_user_id.extend(review_user_id_list)
    review_user_date.extend(review_user_date_list)
    review_user_star.extend(review_user_star_list)
    # review_user_content.extend(review_user_content_list)

# }
driver.quit()

# 리뷰 정보 저장
dic = {'name': review_user_name, 'id': review_user_id,
       'date': review_user_date, 'star': review_user_star}
df = pd.DataFrame(dic)
df.to_csv('reviews\\'+product_id+'.csv', index=False, encoding='utf-8-sig')
