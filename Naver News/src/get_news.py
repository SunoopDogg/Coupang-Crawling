import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

tiles = []
thumbnails = []
contents = []
companies = []
dates = []

search = input('search: ')  # 검색어 입력

for page in range(1001, 1100, 10):
    url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=" + \
        search + "&sort=1&start=" + str(page)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('ul', {'class': 'list_news'})
    news_list = table.find_all('li', {'class': 'bx'})

    print('page: ', page)

    for news in news_list:
        tiles.append(news.find('a', {'class': 'news_tit'}).text)
        thumbnail = news.find('img', {'class': 'thumb api_get'})
        thumbnails.append(thumbnail['src'] if thumbnail else '')
        content = news.find('a', {'class': 'api_txt_lines dsc_txt_wrap'})
        contents.append(content.text if content else '')
        company = news.find('a', {'class': 'info press'})
        companies.append(company.text if company else '')
        date = news.find('span', {'class': 'info'}).text
        if '분' in date or '시간' in date:
            date = datetime.now().strftime("%Y.%m.%d.")
        elif '일' in date:
            date = datetime.now().strftime("%Y.%m.") + \
                str(int(datetime.now().strftime("%d")) - int(date[0])) + '.'
        dates.append(date)

df = pd.DataFrame({'title': tiles, 'thumbnail': thumbnails,
                  'content': contents, 'company': companies, 'date': dates})
df.to_csv('Naver News\\news\\'+search+'.csv', encoding='utf-8-sig')
