import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup


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
    sd = start_year + '.' + start_month + '.' + start_day
    ed = end_year + '.' + end_month + '.' + end_day
    sd1 = start_year + start_month + start_day
    ed1 = end_year + end_month + end_day

    url = "https://search.naver.com/search.naver?where=news&query=" + search + "&sort=1&ds=" + \
        sd + "&de=" + ed + "&nso=so%3Ar%2Cp%3Afrom" + \
        sd1 + "to" + ed1 + "%2Ca%3A"

    while True:  # {
        print(url)

        # 페이지 요청
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 뉴스 존재 여부 확인
        try:
            pages = soup.find('div', {'class': 'sc_page_inner'}).find_all(
                'a',  {'class': 'btn'})
        except:
            print('no pages')
            break

        # 뉴스 목록 가져오기
        table = soup.find('ul', {'class': 'list_news'})
        news_list = table.find_all('li', {'class': 'bx'})

        for news in news_list:  # {
            tiles.append(news.find('a', {'class': 'news_tit'}).text)    # 뉴스 제목
            thumbnail = news.find('img', {'class': 'thumb api_get'})
            thumbnails.append(thumbnail['src'] if thumbnail else '')    # 썸네일
            content = news.find('a', {'class': 'api_txt_lines dsc_txt_wrap'})
            contents.append(content.text if content else '')        # 뉴스 내용
            company = news.find('a', {'class': 'info press'})
            companies.append(company.text if company else '')   # 언론사
            # 날짜 전처리
            date = news.find('span', {'class': 'info'}).text
            if '초' in date or '분' in date or '시간' in date:
                date = datetime.now().strftime("%Y.%m.%d.")
            elif '일' in date:
                date = datetime.now().strftime("%Y.%m.") + \
                    str(int(datetime.now().strftime(
                        "%d")) - int(date[0])) + '.'
            dates.append(date)  # 날짜
        # }

        # 다음 페이지 URL 가져오기 (다음 페이지가 없으면 종료)
        now_page = [page for page in pages if page['aria-pressed']
                    == 'true'][0].text
        next_page = [page for page in pages if page.text ==
                     str(int(now_page) + 1)]
        try:
            url = 'https://search.naver.com/search.naver' + \
                next_page[0]['href']
        except:
            break
    # }

    # 크롤링 결과 저장
    df = pd.DataFrame({'title': tiles, 'thumbnail': thumbnails,
                       'content': contents, 'company': companies, 'date': dates})
    df.to_csv('Naver News\\news\\'+search+'.csv', encoding='utf-8-sig')
# }


if __name__ == '__main__':  # {
    get_news()
# }
