# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class ProductScraperPipeline:
    def __init__(self):
        client = MongoClient()
        self.mongo_base = client['LeroyMerlen']

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        if collection.count_documents({}):
            collection.update_one(
                {'url': item['url']},
                {'$set': item},
                upsert=True
            )
        else:
            collection.insert_one(item)
        return item


class LeroyPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['images']:
            for image in item['images']:
                try:
                    yield scrapy.Request(image)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['images'] = [itm[1] for itm in results if itm[0]]
        return item
