# Сюда получаем данные для их сложной обработки
# Сейчас только скачиваем фотографии

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.castorama_dz


    def process_item(self, item, spider):
        # Сохранение в БД

        if self.mongo_base['url'] != item['url']:
            collection = self.mongo_base[spider.name]
            collection.insert_one(item)
        # return item

class JobPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # Если фото есть, то
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)   # Выполняем запрос по ссылке
                except Exception as e:
                    print(e)
    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

