# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json

import codecs
from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.exceptions import DropItem
#from scrapy.pipelines.images import ImagesPipeline
import time
import MySQLdb
import MySQLdb.cursors

class HupuPipeline(object):
    
    def __init__(self):
        try:
            self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                                host = 'localhost',
                                                db = 'test',
                                                user = 'root',
                                                passwd = '',
                                                cursorclass = MySQLdb.cursors.DictCursor,
                                                charset = 'utf8',
                                                use_unicode = True
                                                )
        except:
            raise
        

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item):
        if item.get('title'):
            #print '******************'
            #$print item.get('title')
            #print '******************'
            try:
                tx.execute(\
                    "INSERT INTO topics(title, author, url, content, light) VALUES(%s, %s, %s, %s, %s)",
                    (item['title'][0],
                     item['author'][0],
                     item['url'],
                     item['content'][0:-1],
                     item['light'])
                    )
            except:
                raise
    def handle_error(self, e):
        log.msg(e)
