from math import prod
from time import sleep
from init_craw import *
from bs4 import BeautifulSoup
import pandas as pd

# 검색 상품 입력
search = input('search: ')
search = search.replace(' ', '+')

init_craw()
driver = get_driver(get_path())
driver.set_window_position(0, 0)
driver.set_window_size(1920, 1080)

products_id = []
products_name = []
products_price = []
products_url = []

for page in range(1, 11):  # {
    url = 'https://www.coupang.com/np/search?component=&q='+search+'&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page=' + \
        str(page)+'&rocketAll=false&searchIndexingToken=1=6&backgroundColor='

    driver.get(url)
    driver.implicitly_wait(10)

    # 상품 페이지 소스 가져오기
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.select('li.search-product')  # 상품 리스트
    products_id_list = [product.get('data-product-id')
                        for product in products]  # 상품 id
    products_name_list = [product.select_one('div.name').get_text()
                          for product in products]  # 상품 이름
    products_price_list = []    # 상품 가격
    for product in products:    # {
        price = product.select_one('strong.price-value')
        if price is not None:
            products_price_list.append(price.get_text())
        else:
            products_price_list.append('0')
    # }
    products_url_list = [product.select_one(
        'a.search-product-link').get('href') for product in products]   # 상품 url

    products_id.extend(products_id_list)
    products_name.extend(products_name_list)
    products_price.extend(products_price_list)
    products_url.extend(products_url_list)
# }
driver.quit()

# 상품 정보 저장
dic = {'id': products_id, 'name': products_name,
       'price': products_price, 'url': products_url}
df = pd.DataFrame(dic)
df.to_csv('products\\'+search+'.csv', encoding='utf-8-sig')
