# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


import scrapy


class InsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    article_id = scrapy.Field()
    username = scrapy.Field()
    img_src = scrapy.Field()
    content = scrapy.Field()
    comments = scrapy.Field()
