# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QueryItem(scrapy.Item):
    # define the fields for your item here like:
    keyword = scrapy.Field()
    pass


class ResultItem(scrapy.Item):
    # define the fields for your item here like:
    domain = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    keyword = scrapy.Field()
    crawledDate = scrapy.Field()
    aliveDate = scrapy.Field()
    job = scrapy.Field()
    pass
