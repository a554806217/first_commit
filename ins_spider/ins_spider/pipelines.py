# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
from pymysql import cursors
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

class InsSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class TwistedMysqlPipeline(object):
    @classmethod
    def from_settings(cls,settings):
        db_prams = dict(
        host=settings['MYSQL_HOST'],
        user=settings['MYSQL_USER'],
        password=settings['MYSQL_PW'],
        db=settings['MYSQL_DB'],
        port=3306,
        use_unicode=True,
        charset=settings['MYSQL_CHARSET'],
        cursorclass=cursors.DictCursor
        )
        db_pool = adbapi.ConnectionPool('pymysql',**db_prams)
        return cls(db_pool)
    def __init__(self, dbpool):
        self.db_pool = dbpool

    def process_item(self,item,spider):
        query = self.db_pool.runInteraction(self.insert_item, item)
        query.addErrback(self.handle_error, item,spider)
        return item
    def handle_error(self,failure,item,spider):
        print('报错了...')
        print(failure)
        print(item)

    def insert_item(self, cursor, item):
        sql = "INSERT INTO ins_people(id,article_id,username,content,comments)VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(sql, (item['id'], item['article_id'],item['username'], item['content'], item['comments']))


class Imgpipipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        reqs = [Request(x,meta={'item': item}) for x in item.get(self.images_urls_field,[])]
        return reqs
    def file_path(self, request, response=None, info=None):
        item = request.meta.get('item')
        alt = item['username']
        name = item['img_src'][0].split('/')[-1]
        path = alt + '/' + name
        return path