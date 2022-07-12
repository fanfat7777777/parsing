from lxml import html
import requests
from pymongo import MongoClient
from pprint import pprint

# БД
client = MongoClient('127.0.0.1', 27017)
db = client['news']
news_db = db.news

# Парсер
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'}

url = 'https://lenta.ru/'

session = requests.Session()
response = session.get(url, headers=headers)

dom = html.fromstring(response.text)
items = dom.xpath("//*[contains(@class, '_topnews')]")

repeats_news = []
for item in items:
    new = {}
    name = item.xpath("./*[contains(@class, 'card-')]//*[contains(@class, '__title')]/text()")
    time = item.xpath(".//*[contains(@class, '__date')]/text()")
    href = item.xpath("./@href")

    new['Название'], new['Время'], new['Ссылка']= name, time, href

    news_db.insert_one(new) if news_db.find_one({'Ссылка': href}) == None else repeats_news.append(new)

for item in news_db.find({}):
    pprint(item)

print()
print('#'*5*15)
print(f'Повторы: {len(repeats_news)}')
pprint(repeats_news) if len(repeats_news) > 0 else None
