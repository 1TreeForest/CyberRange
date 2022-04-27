# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpecialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 电影名
    name = scrapy.Field()
    # 详情页
    link = scrapy.Field()
    # 爬取的电影网站
    site = scrapy.Field()
    crawledDate = scrapy.Field()
    pass


class UniversalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 电影名
    name = scrapy.Field()
    # 详情页
    link = scrapy.Field()
    # 爬取的电影网站
    site = scrapy.Field()
    crawledDate = scrapy.Field()
    pass


class FriendLinkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 网站名
    name = scrapy.Field()
    # 链接
    link = scrapy.Field()
    domain = scrapy.Field()
    pass
