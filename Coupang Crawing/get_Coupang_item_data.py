from init_craw import *
from bs4 import BeautifulSoup

init_craw()
driver = get_driver(get_path())

url = 'https://www.coupang.com/np/search?q=%EC%95%84%EC%9D%B4%ED%8F%B0&channel=recent'
driver.get(url)
driver.implicitly_wait(10)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

driver.quit()

item_name = soup.select('div.name')
item_names = [name.get_text() for name in item_name]

print(item_names)
