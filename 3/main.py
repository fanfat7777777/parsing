import requests
from bs4 import BeautifulSoup
import time
import random
import re
from pprint import pprint
import pymongo
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['vacancy']
vacancy_bd = db.vacancy


page = 0
url = f'https://kirov.hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113&hhtmFrom=main'

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'}
params = {'page': f'{page}',
          'items_on_page': 20}
response = session.get(url, headers=headers, params=params)

dom = BeautifulSoup(response.text, 'html.parser')

# Узнаём количество страниц
page = dom.select('span.pager-item-not-in-short-range a.bloko-button span')
for p in page[:]:
    if p.text.isdigit():
        page = int(p.text)
#print(page)

#vacancy = page.select('div.vacancy-serp-item')
vacancy_list = []
# Идём по страницам page + 1
while page >= 0:
    print(f'Страница {page}')
    # Задержка при проходе
    value = random.random()
    scaled_value = 1 + (value * (9 - 5))
    # print(scaled_value)
    time.sleep(scaled_value)

    params = {'page': f'{page}'}
    response = session.get(url, headers=headers, params=params)
    dom = BeautifulSoup(response.text, 'html.parser')
    # print(response.url)

    # Задаём поиск
    result_vacancy = dom.select('div.vacancy-serp-item')

    for vacancy in result_vacancy:
        vacancy_data = {}
        name = vacancy.find('a', {'class': 'bloko-link'})  # Наименование вакансии
        payment = vacancy.find('span', {'class': 'bloko-header-section-3'})  # Блок с оплатой
        vacancy_url = vacancy.find('a', {'class': 'bloko-link'}).get('href')  # Ссылка на вакансию
        website = response.url  # Получаем адрес страницы

        # Добавляем данные по вакансии
        vacancy_data['Название'] = name.text

        if payment == None:
            vacancy_data['Минимальная'] = 'None'
            vacancy_data['Максимальная'] = 'None'
            vacancy_data['Валюта'] = ''
        else:
            payment = payment.text.replace('\u202f', ' ')
            search = "\d{1,3}([' ']|[' '])\d?\d?\d?"    # "(\d[\d]{1,2}([' ']|[' '])[\d]{3})"
            # \d{1,3}([' ']|[' '])\d?\d?\d?
            if payment[:2] == 'от':
                currency = re.search(r'(\D*)$', payment).group(0).replace(' ', '')
                payment = re.search(rf"{search}", payment)

                vacancy_data['Минимальная'] = int(payment.group(0).replace(' ', ''))
                vacancy_data['Максимальная'] = 'None'
                vacancy_data['Валюта'] = currency
            elif payment[:2] == 'до':
                currency = re.search(r'(\D*)$', payment).group(0).replace(' ', '')
                payment = re.search(rf"{search}", payment)
                vacancy_data['Минимальная'] = 'None'
                vacancy_data['Максимальная'] = int(payment.group(0).replace(' ', ''))
                vacancy_data['Валюта'] = currency
            else:
                #print(payment)
                currency = re.search(r'(\D*)$', payment).group(0).replace(' ', '')
                vacancy_data['Минимальная'] = int(re.search(r"\d{1,3}([' ']|[' '])\d?\d?\d?", payment).group(0).replace(' ', '').replace(' ', ''))
                vacancy_data['Максимальная'] = int(re.search(rf"{search}", payment[len(re.search(r"\d{1,3}([' ']|[' '])\d?\d?\d?", payment).group(0)):]).group(0).replace(' ', '').replace(' ', ''))
                vacancy_data['Валюта'] = currency

        vacancy_data['Сылка на вакансию:'] = vacancy_url
        vacancy_data['Откуда взято:'] = (website)



        if vacancy_bd.find_one({'Сылка на вакансию:': vacancy_data['Сылка на вакансию:']}) == None:
            vacancy_bd.insert_one(vacancy_data)

        else:
            vacancy_bd.replace_one({'Сылка на вакансию:': f"{vacancy_data['Сылка на вакансию:']}"}, vacancy_data)

    page -= 1


#print(len(vacancy_list))
#pprint(vacancy_list)

money = int(input('Введите минимальную зп: '))

for item in vacancy_bd.find({'$or': [{'Минимальная': {'$gt': money},
                                      'Максимальная': {'$gt': money}}]}):
    pprint(item)
