# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


db_info = {"ip":"localhost", "port":27017, "db_name":"news", 
            "collection":"wangyi"}

class NewsPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(db_info['ip'], db_info['port'])
        self.db = self.client[db_info['db_name']]
        self.db[db_info['collection']].remove()

    def process_item(self, item, spider):
        self.db[db_info['collection']].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
