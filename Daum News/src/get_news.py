import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


def get_news():  # {
    tiles = []
    thumbnails = []
    contents = []
    companies = []
    dates = []

    search = input('search: ')  # 검색어 입력

    # 검색 기간 입력
    start_year = input('start year: ')
    start_month = input('start month: ')
    start_day = input('start day: ')
    end_year = input('end year: ')
    end_month = input('end month: ')
    end_day = input('end day: ')

    # 검색 기간 URL 적용 전처리
    sd = start_year + start_month + start_day+'000000'
    ed = end_year + end_month + end_day+'235959'

    url = "https://search.daum.net/search?w=news&q=" + search + \
        "&sort=recency&p=1" + "&sd=" + sd + "&ed=" + ed

    # 페이지 요청
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 뉴스 개수 가져오기
    cnt_news = soup.find('span', {'class': 'txt_info'}).text
    cnt_news = int(cnt_news.split(
        '/')[1].replace('건', '').replace(',', '').strip())

    for page in range(1, 1+int(cnt_news/10)+(0 if cnt_news % 10 == 0 else 1), 1):   # {
        url = "https://search.daum.net/search?w=news&q=" + search + \
            "&sort=recency&p=" + str(page) + "&sd=" + sd + "&ed=" + ed

        print(url)
        print('page: ', page)

        # 페이지 요청
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 뉴스 목록 가져오기
        table = soup.find('ul', {'class': 'list_news'})
        news_list = table.find_all('li')

        for news in news_list:  # {
            tiles.append(news.find('a', {'class': 'tit_main'}).text)    # 뉴스 제목
            thumbnail = news.find('img')
            thumbnails.append(
                thumbnail['src'] if thumbnail else '')    # 썸네일 이미지
            content = news.find('p', {'class': 'desc'})
            contents.append(content.text if content else '')        # 뉴스 내용
            company = news.find_all('span', {'class': 'f_nb'})[0]
            companies.append(company.text if company else '')     # 언론사
            # 날짜 전처리
            date = news.find_all('span', {'class': 'f_nb'})[1].text
            if '초' in date or '분' in date or '시간' in date:
                date = datetime.now().strftime("%Y.%m.%d.")
            elif '일' in date:
                date = datetime.now().strftime("%Y.%m.") + \
                    str(int(datetime.now().strftime(
                        "%d")) - int(date[0])) + '.'
            dates.append(date)                                    # 날짜
        # }
    # }

    # 크롤링 결과 저장
    df = pd.DataFrame({'title': tiles, 'thumbnail': thumbnails,
                       'content': contents, 'company': companies, 'date': dates})
    df.to_csv('Daum News\\news\\'+search+'.csv', encoding='utf-8-sig')
# }


if __name__ == '__main__':  # {
    get_news()
# }
