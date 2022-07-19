# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
#import re


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies_hhru


    def process_item(self, item, spider):
        # Если ссылки не равны
        if self.mongo_base['url'] != item['url']:
            item['salary'] = self.process_salary(item['salary'])
            collection = self.mongo_base[spider.name]
            collection.insert_one(item)

    def process_salary(self, salary):
        min, max, cur, taxes = None, None, None, None
        if len(salary) == 1:
            pass
        elif salary[0].strip().lower() == 'от' and salary[2].strip().lower() == 'до':
            min, max, cur, taxes = salary[1], salary[3], salary[5], salary[7]
            #search = re.search('\D{3}', salary[3])
            #print(int(salary[3].replace(f"{search}", "").replace(" ", "").replace(r"\xa", "")))
            #print(salary[3].strip())
        elif salary[0].strip().lower() == 'от' and salary[0].strip().lower() != 'до':
            min, max, cur, taxes = salary[1], None, salary[3], salary[5]

        elif salary[0].strip().lower() == 'до' and salary[0].strip().lower() != 'от':
            min, max, cur, taxes = None, salary[1], salary[3], salary[5]


        return {'Минимальная': min, 'Максимальная': max, 'Валюта': cur, 'Налоги': taxes}
