
import requests
from lxml import html
from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import DuplicateKeyError

#TASK 1

header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"}
# header ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'}

response = requests.get('https://lenta.ru', headers =  header)
pprint(response)
dom = html.fromstring(response.text)
pprint(dom)

items = dom.xpath("//div[contains(@class, 'topnews')]//a")
items_list = []
for item in items:
    item_info = {}
    info = item.xpath("./div/span/text()")
    href = item.xpath("./@href")
    time_p = item.xpath("./div/div/time/text()")
    item_info['info'] = info
    item_info['href'] = href
    item_info['time'] = time_p
    item_info['_id'] = href[0]
    items_list.append(item_info)

pprint(items_list)


#TASK 2

client = MongoClient('127.0.0.1', 27017)

db = client['db_news']
news = db.news


def add_news(th_news):
    try:
        news.insert_one(th_news)
    except DuplicateKeyError:
        print('New is already exist')


for item_news in items_list:
    add_news(item_news)


