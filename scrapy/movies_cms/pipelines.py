# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

# from scrapy import log
from urllib.parse import quote_plus
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem


class MoviesCmsPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        uri = "mongodb://%s:%s@%s:%s" % (quote_plus(settings['MONGODB_USER']), quote_plus(
            settings['MONGODB_PASS']), settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        connection = pymongo.MongoClient(uri)
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))

        return item
