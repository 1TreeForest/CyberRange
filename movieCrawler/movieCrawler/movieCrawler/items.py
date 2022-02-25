# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviecrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #电影名
    name = scrapy.Field()
    #详情页
    link = scrapy.Field()
    #爬取的电影网站
    site = scrapy.Field()
    pass
