"""
Написать программу, которая собирает входящие письма
из своего или тестового почтового ящика и сложить данные
о письмах в базу данных (от кого, дата отправки, тема письма,
текст письма полный)
"""
import time
from datetime import datetime, timedelta

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(
    executable_path='./chromedriver.exe', options=chrome_options
)
driver.get('https://mail.ru/')

mail = driver.find_element_by_class_name('email-input')
mail.send_keys('study.ai_172@mail.ru')
mail.send_keys(Keys.ENTER)

time.sleep(1)

password = driver.find_element_by_class_name('password-input')
password.send_keys('NextPassword172!?')
password.send_keys(Keys.ENTER)

time.sleep(5)

mail_quantity = int(driver.find_element_by_class_name(
    'nav__item').get_attribute('title').split(' ')[1])

data = []
i = 1
while True:
    result = {}
    try:
        mails = WebDriverWait(driver, 20)
        mails.until(ec.element_to_be_clickable(
            (By.CLASS_NAME, 'js-tooltip-direction_letter-bottom')))
    except Exception:
        continue

    actions = ActionChains(driver)
    actions.send_keys(Keys.DOWN).send_keys(Keys.ENTER)
    actions.perform()

    try:
        wait_from_user = WebDriverWait(driver, 20)
        wait_from_user.until(ec.element_to_be_clickable(
            (By.CLASS_NAME, 'letter-contact')))
    except Exception:
        continue

    from_user = driver.find_element_by_class_name(
        'letter-contact').get_attribute('title')
    date_text = driver.find_element_by_class_name('letter__date').text
    if date_text.split(',')[0] == 'Сегодня':
        date = datetime.now().replace(hour=0, minute=0, second=0)
        time_ = date_text.split(' ')[-1].split(':')
        time_delta = timedelta(hours=int(time_[0]), minutes=int(time_[1]))
        date_time = date + time_delta
    elif date_text.split(',')[0] == 'Вчера':
        date = datetime.now().replace(
            hour=0, minute=0, second=0) - timedelta(hours=24)
        time_ = date_text.split(' ')[-1].split(':')
        time_delta = timedelta(hours=int(time_[0]), minutes=int(time_[1]))
        date_time = date + time_delta
    else:
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
        month = date_text.split(' ')[1].split(',')[0]
        new_date = date_text.replace(month, months[month])
        date_time = datetime.strptime(f'2021 {new_date}',
                                      '%Y %d %m, %H:%M')
    # Как только будут письма прошлого года, нужно будет добавить

    subject = driver.find_element_by_class_name('thread__subject').text

    content = driver.find_element_by_class_name('letter-body__body').text

    result['from_user'] = from_user
    result['date_time'] = date_time
    result['subject'] = subject
    result['content'] = content

    data.append(result)

    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    i += 1
    if i > mail_quantity:
        break

client = MongoClient()
db = client['mail'].mail

if db.count_documents({}):
    for document in data:
        db.update_one(
            {
                'date_time': document['date_time'],
                'from_user': document['from_user'],
                'subject': document['subject'],
                'content': document['content']
            },
            {'$set': document},
            upsert=True,
        )
else:
    db.insert_many(data)
