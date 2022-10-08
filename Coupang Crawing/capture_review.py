from selenium.webdriver.common.by import By


def get_name_index(user_name, review_user_name_list):  # {
    if (user_name in review_user_name_list):
        return review_user_name_list.index(user_name)
    else:
        return -1
# }


def is_content_contain(content_target, review_content_list):  # {
    count = 0

    for content in content_target:
        if content in review_content_list:
            count += 1

    print('count=', count)
    if count == len(content_target):
        return True
    else:
        return False
# }


def get_target_element(driver, index):  # {
    return driver.find_elements(By.CSS_SELECTOR, 'article.sdp-review__article__list')[index]
# }


def capture_review(user_name, product_id, element):  # {
    # 리뷰 캡쳐
    element_png = element.screenshot_as_png
    with open('captures\\'+user_name+'_'+product_id+'.png', 'wb') as file:
        file.write(element_png)
# }
