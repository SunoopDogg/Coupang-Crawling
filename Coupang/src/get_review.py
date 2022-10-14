import time
import pandas as pd
from init_craw import *
from capture_review import *
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 쿠팡 상품 ID 입력
product_id = input("product_id: ")
user_name = '김*옥'  # input("user_name: ")
content_target = ['']

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

# 최신순 클릭
wait = WebDriverWait(driver, 5)
wait.until(EC.element_to_be_clickable(
    (By.CLASS_NAME, 'sdp-review__article__order__sort__newest-btn'))).click()
driver.implicitly_wait(10)
time.sleep(1)

review_name = []
review_id = []
review_date = []
review_star = []
review_content = []


index = 0
while True:  # {
    if (index == 10):
        break

    # 리뷰 페이지 소스 가져오기
    review_page_button = driver.find_elements(
        By.CLASS_NAME, 'sdp-review__article__page__num')

    # 리뷰 페이지 클릭
    print('data-page=', review_page_button[index].get_attribute('data-page'))
    review_page_button[index % 10].click()
    driver.implicitly_wait(10)
    time.sleep(2)
    index += 1

    # 리뷰 페이지 리소스 가져오기
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    reviews = soup.select('article.sdp-review__article__list')  # 리뷰 리스트
    # print('reviews=', reviews)
    review_name_list = [review.select_one(
        'span.sdp-review__article__list__info__user__name').get_text(strip=True) for review in reviews]  # 리뷰 작성자 이름
    review_id_list = [review.select_one('span.sdp-review__article__list__info__user__name')[
        'data-member-id'] for review in reviews]    # 리뷰 작성자 ID
    review_date_list = [review.select_one(
        'div.sdp-review__article__list__info__product-info__reg-date').get_text() for review in reviews]  # 리뷰 작성일
    review_star_list = [review.select_one('div.sdp-review__article__list__info__product-info__star-orange')[
        'data-rating'] for review in reviews]  # 리뷰 별점
    review_content_list = []  # 리뷰 내용
    for review in reviews:  # {
        content = review.select_one(
            'div.sdp-review__article__list__review__content')
        if content is not None:
            review_content_list.append(content.get_text(strip=True))
        else:
            review_content_list.append('')
    # }

    print(review_name_list)

    review_name.extend(review_name_list)
    review_id.extend(review_id_list)
    review_date.extend(review_date_list)
    review_star.extend(review_star_list)
    review_content.extend(review_content_list)

    name_index = get_name_index(user_name, review_name_list)
    if (name_index != -1 and is_content_contain(content_target, review_content_list[name_index])):
        element = get_target_element(driver, name_index)
        driver.execute_script("window.scrollTo({}, {})".format(
            element.location['x'], element.location['y']-50))
        capture_review(user_name.replace('*', 'x'), product_id, element)
        time.sleep(1)
# }
driver.quit()

# 리뷰 정보 저장
dic = {'name': review_name, 'id': review_id,
       'date': review_date, 'star': review_star, 'content': review_content}
df = pd.DataFrame(dic)
df.to_csv('Coupang\\reviews\\'+product_id+'.csv', encoding='utf-8-sig')
