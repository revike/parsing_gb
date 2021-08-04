"""
1. Написать функцию, которая будет добавлять в вашу базу
данных только новые вакансии с сайта.

2. Написать функцию, которая производит поиск и выводит
на экран вакансии с заработной платой больше введённой суммы.
"""
from pprint import pprint
from pymongo import MongoClient
from hw_2.hw_2 import run


def add_db_vacancy(db_name, vacancy):
    """Добавление вакансий в базу данных"""
    client = MongoClient()
    db = client[db_name]
    data = run(vacancy)
    collection = db.vacancies
    if collection.count_documents({}):
        for document in data:
            collection.update_one(
                {'link': document['link']},
                {'$set': document},
                upsert=True,
            )
    else:
        collection.insert_many(data)
    return collection


def get_search_data(collection, value):
    """Поиск вакансий"""
    collections = collection.find(
        {
            'salary.min_salary': {
                '$gt': value
            }
        }
    )

    for vacancy in collections:
        pprint(vacancy)


if __name__ == '__main__':
    coll = add_db_vacancy('vacancies', 'python')
    get_search_data(coll, 100000)
