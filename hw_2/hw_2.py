import json

from bs4 import BeautifulSoup as bS
import requests
from pprint import pprint


def get_page(text: str):
    """Получение количество страниц hh.ru"""
    url = 'https://hh.ru/'

    params = {
        'L_save_area': 'true',
        'clusters': 'true',
        'enable_snippets': 'true',
        'text': text,
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 '
                      '(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    response = requests.get(
        f'{url}search/vacancy', params=params, headers=headers)

    soup = bS(response.text, 'html.parser')

    try:
        page = int(soup.find_all('a', attrs={'class': 'bloko-button'})[
                       -2].findChildren()[0].getText())
    except ValueError:
        page = 1

    result = {
        'url': url,
        'params': params,
        'headers': headers,
        'page': page
    }

    return result


def get_data(**kwargs):
    """Получение данных с hh.ru"""
    vacancies = []
    for i in range(0, kwargs['page']):
        kwargs['params']['page'] = str(i)
        response = requests.get(
            f'{kwargs["url"]}search/vacancy',
            params=kwargs['params'], headers=kwargs['headers']
        )

        soup = bS(response.text, 'html.parser')

        vacancy_list = soup.find_all('div',
                                     attrs={'class': 'vacancy-serp-item'})

        for vacancy in vacancy_list:
            vacancy_data = {}
            vacancy_name = vacancy.find('a', attrs={
                'class': 'bloko-link'
            }).getText()

            vacancy_link = vacancy.find('a', attrs={
                'class': 'bloko-link'
            }).get('href')

            vacancy_salary = vacancy.find('span', attrs={
                'data-qa': 'vacancy-serp__vacancy-compensation'
            })

            salary_data = {}
            if vacancy_salary:
                vacancy_salary = vacancy_salary.getText()
                salary_split = vacancy_salary.split(' ')
                try:
                    min_salary = float(
                        ''.join(salary_split[0].split('\u202f')))
                    max_salary = float(
                        ''.join(salary_split[2].split('\u202f')))
                    salary_data['min_salary'] = min_salary
                    salary_data['average'] = (max_salary + min_salary) / 2
                    salary_data['max_salary'] = max_salary
                except ValueError:
                    salary = float(''.join(salary_split[1].split('\u202f')))
                    salary_data['min_salary'] = salary
                    salary_data['average'] = salary
                    salary_data['max_salary'] = salary

            vacancy_data['name'] = vacancy_name
            vacancy_data['salary'] = salary_data
            vacancy_data['link'] = vacancy_link
            vacancy_data['site'] = kwargs['url']

            vacancies.append(vacancy_data)

    return vacancies


def save_data(data, text):
    """Сохранение данных в *.json"""
    with open(f'data_{text}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def run(text):
    """Запуск парсинга"""
    pages = get_page(text)
    data = get_data(
        url=pages['url'],
        params=pages['params'],
        headers=pages['headers'],
        page=pages['page']
    )
    save_data(data, text)
    pprint(data)


if __name__ == '__main__':
    """Текст для поиска вакансий"""
    run('python')
