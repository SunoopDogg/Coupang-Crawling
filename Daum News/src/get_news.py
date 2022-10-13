import time
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

for page in range(1, 10, 1):
    url = "https://search.daum.net/search?nil_suggest=btn&w=news&DA=STC&q=" + \
        search + "&sort=recency&p=" + str(page)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('ul', {'class': 'list_news'})
    news_list = table.find_all('li')

    print('page: ', page)

    for news in news_list:
        tiles.append(news.find('a', {'class': 'tit_main'}).text)
        thumbnail = news.find('img')
        thumbnails.append(thumbnail['src'] if thumbnail else '')
        content = news.find('p', {'class': 'desc'})
        contents.append(content.text if content else '')
        company = news.find_all('span', {'class': 'f_nb'})[0]
        companies.append(company.text if company else '')
        date = news.find_all('span', {'class': 'f_nb'})[1].text
        if '초' in date or '분' in date or '시간' in date:
            date = datetime.now().strftime("%Y.%m.%d.")
        elif '일' in date:
            date = datetime.now().strftime("%Y.%m.") + \
                str(int(datetime.now().strftime("%d")) - int(date[0])) + '.'
        dates.append(date)

df = pd.DataFrame({'title': tiles, 'thumbnail': thumbnails,
                  'content': contents, 'company': companies, 'date': dates})
df.to_csv('Daum News\\news\\'+search+'.csv', encoding='utf-8-sig')
