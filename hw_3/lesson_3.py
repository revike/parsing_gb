from pprint import pprint

from pymongo import MongoClient

client = MongoClient()
db = client['db_new_test']

persons = db.persons

# persons.insert_one(
#     {
#         'author': 'Peter',
#         'age': 29,
#         'text': 'is cool!',
#         'tags': ['cool', 'hot', 'ice'],
#         'date': '14.06.2020',
#     }
# )

# persons.insert_many(
#     [
#         {
#             'author': 'John',
#             'age': 24,
#             'text': 'is bad!',
#             'tags': ['cool', 'hot', 'ice'],
#             'date': '15.06.2020',
#         },
# {
#             'author': 'Make',
#             'age': 33,
#             'text': 'is cool - think about it!',
#             'tags': ['cool', 'hot', 'ice'],
#             'date': '14.06.2020',
#         },
# {
#             'author': 'Nick',
#             'age': 55,
#             'text': 'is cool - the real!',
#             'tags': ['cool', 'hot', 'ice'],
#             'date': '14.06.2020',
#         },
#     ]
# )


# for doc in persons.find(
#         {
#             'author': 'Peter',
#             'age': 29
#         }
# ):
#     pprint(doc)

# for doc in persons.find(
#         {
#             'age': {
#                 '$lt': 30
#             }
#         }
# ):
#     pprint(doc)

# for doc in persons.find(
#         {
#             '$or': [
#                 {
#                     'author': 'Peter',
#                 },
#                 {
#                     'age': 33
#                 }
#             ]
#         }
# ):
#     pprint(doc)

# for doc in persons.find(
#         {
#             'age': {
#                 '$lt': 30
#             }
#         },
#         {
#             'author': 1,
#             'age': 1,
#             '_id': 0
#         }
# ).limit(2):
#     pprint(doc)

# for doc in persons.find({}).sort('age', -1):  # -1 это по убыванию
#     pprint(doc)

for doc in persons.find(
        {
            'author': 'Peter',
        },
        {
            'author': 1,
            'age': 1,
            '_id': 0
        }
):
    pprint(doc)

persons.update_one(  # обновить
    {
        'author': 'Peter'
    },
    {
        '$set': {
            'age': 15
        }
    }
)

for doc in persons.find(
        {
            'author': 'Peter',
        },
        {
            'author': 1,
            'age': 1,
            '_id': 0
        }
):
    pprint(doc)

# persons.replace_one({'author': 'peter'}, doc)  # перезаписать

# persons.delete_one({'author': 'Peter'})
# persons.delete_many({'author': 'Peter'})

count = persons.count_documents({})  # количество
print(count)
