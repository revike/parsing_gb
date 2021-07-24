import json
import requests
from pprint import pprint


def save_data(data, user):
    """Сохранение данных в *.json"""
    with open(f'data_{user}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_data_github(user):
    """Получение данных с github.com"""
    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      'AppleWebKit/537.36 (KHTML, like Gecko)'
                      'Chrome/91.0.4472.164 Safari/537.36'
    }
    url = f'https://api.github.com/users/{user}/repos'
    response = requests.get(url, headers=my_headers).json()
    save_data(response, user)
    return response


def get_repo(user):
    """Получение списка репозиториев"""
    repositories = []
    data_github = get_data_github(user)
    for repo in data_github:
        repositories.append(repo['name'])
    return repositories


if __name__ == '__main__':
    """Запишите в `user` имя пользователя с github.com для получения списка 
    репозиториев и файла *.json с данными """
    user = 'revike'
    result = get_repo(user)
    pprint(result)
