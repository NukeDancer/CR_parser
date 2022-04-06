# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
import pymongo
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


class CrParserPipeline:
    def __init__(self):
        connection = pymongo.MongoClient('10.0.0.70', 27017)
        self.db = connection.Castorama

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        collection.insert_one(item)
        return item


class CrParserImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['image_urls']:
            for img_url in item['image_urls']:
                try:
                    yield scrapy.Request(img_url)
                except Exception as err:
                    print(err)

    def item_completed(self, results, item, info):
        item['image_urls'] = [el[1] for el in results if el[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        sub_dir = item['name'].replace('/', '-')
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{sub_dir}/{image_guid}.jpeg'
