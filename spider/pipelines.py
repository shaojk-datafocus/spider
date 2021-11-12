# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import pymongo
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class JsonPipeline:
    def __init__(self, file_name="result"):
        if not file_name.endswith(".json"):
            file_name+=".json"
        self.file_name = file_name
        self.is_first = True

    def open_spider(self, spider):
        if hasattr(spider, "output_path"):
            self.file_name = spider.output_path
        self.f = open(self.file_name, 'a', encoding='utf-8')
        self.f.write("[")

    def close_spider(self, spider):
        self.f.write("]")
        self.f.close()

    def process_item(self, item, spider):
        if self.is_first:
            self.is_first = False
        else:
            self.f.write(',')
        self.f.write(json.dumps(ItemAdapter(item).asdict()).encode('utf-8').decode('unicode_escape'))
        return item


class SpiderPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        cls.collection = "Test"
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection].insert_one(ItemAdapter(item).asdict())
        return item

class BilibiliPipeline(SpiderPipeline):
    @classmethod
    def from_crawler(cls, crawler):
        cls.collection = "bilibili"
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

class ItemPipeline(SpiderPipeline):
    @classmethod
    def from_crawler(cls, crawler):
        cls.collection = "Item"
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )