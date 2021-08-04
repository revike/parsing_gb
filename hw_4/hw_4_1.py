import requests
from datetime import datetime
from lxml import html
from pymongo import MongoClient


def get_date(date):
    """Получение даты"""
    months = {
        'января': '1',
        'февраля': '2',
        'марта': '3',
        'апреля': '4',
        'мая': '5',
        'июня': '6',
        'июля': '7',
        'августа': '8',
        'сентября': '9',
        'октября': '10',
        'ноября': '11',
        'декабря': '12'
    }

    month = date.split(' ')[-2]
    new_date = date.replace(month, months[month])
    date_utc = datetime.strptime(new_date, ' %H:%M,  %d %m %Y')

    return date_utc


def get_data():
    """Получение данных"""
    url = 'https://lenta.ru/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.107 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    items = dom.xpath('//time[@class="g-time"]')

    news = []
    for item in items:
        new = {}
        link = item.xpath('./../@href')[0]
        name = item.xpath('./../text()')[0]
        source = 'lenta.ru'
        date = item.xpath('./@datetime')[0]

        if link.split('/')[1] == 'news':
            link = f'{url}{link}'

        new['link'] = link
        new['name'] = name
        new['source'] = source
        new['date'] = get_date(date)

        news.append(new)

    return news


def add_db_news(news):
    """Добавление в базу данных"""
    client = MongoClient()
    db = client['news'].news_lenta
    if db.count_documents({}):
        for document in news:
            db.update_one(
                {'link': document['link']},
                {'$set': document},
                upsert=True,
            )
    else:
        db.insert_many(news)


if __name__ == '__main__':
    data = get_data()
    add_db_news(data)
