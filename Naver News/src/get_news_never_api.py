import json
import urllib.request
from bs4 import BeautifulSoup

client_id = "Yt4cKsZNck60cfHDIwOm"
client_secret = "F25Ab1P5c2"

search = input('search: ')  # 검색어 입력
encText = urllib.parse.quote(search)

url = "https://openapi.naver.com/v1/search/news.json?query=" + \
    encText + "&display=100&sort=date"  # JSON 결과
# url = "https://openapi.naver.com/v1/search/news.xml" + encText # XML 결과

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)

response = urllib.request.urlopen(request)

rescode = response.getcode()
if (rescode == 200):
    response_body = response.read()
    with open('Naver News\\news\\'+search+'.json', 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(json.loads(response_body.decode(
            'utf-8')), indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(jsonFile)
else:
    print("Error Code:" + rescode)
