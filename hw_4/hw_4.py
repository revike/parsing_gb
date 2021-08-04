# в response.text приходят непонятные вещи. Яндекс думает что я робот

import requests
from lxml import html


def get_data():
    """Получение данных"""
    url = 'https://yandex.ru/news/region/nizhny_novgorod'

    headers = {
        'User-Agent': 'Mozilla/5.0 '
                      '(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    items = dom.xpath('//article[contains(@class, "mg-card")]')

    for item in items:
        name = item.xpath('.//h2[@class="mg-card__title"]/text()')
        link = item.xpath(
            './/div[@class="mg-card__inner" or @class="mg-card__text"]/a/@href')
        source = item.xpath('.//span[@class="mg-card-source__source"]/a/text()')
        print(name, link, source)


if __name__ == '__main__':
    get_data()
