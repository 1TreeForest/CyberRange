import time

import scrapy
from movieCrawler.items import SpecialItem
import re


class Movie2345Spider(scrapy.Spider):
    name = 'movie_2345'
    allowed_domains = ['dianying.2345.com']
    start_urls = ['http://dianying.2345.com/list/------1.html']
    crawledDate = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    # https://www.bdcmkj.com/ty/1.html


    def parse(self, response):
        # 标题列表
        name = response.xpath('//li//div//span/text()').extract()
        #//li//div/a//@title

        # 详情列表
        link = response.xpath('//div/div/div//li/div//@href').extract()
        #//div//li/div/a/@href


        # 遍历列表，将结果存入items
        for i in range(0, len(name)):
            # 实例化一个item类，然后将结果全部存入items
            item = SpecialItem()
            # 提取出的电影名中包含其他信息，如”2012年喜剧《男人如衣服》720p.BD国粤双语中字“，需进一步使用正则匹配出书名号中的电影名
            item['name'] = name[i]

            # 拼接URL，获取所有电影详情的URL，拼成完整的URL来访问地址
            item['link'] = "http:" + link[i]
            item['site'] = 'dianying.2345.com'
            item['crawledDate'] = self.crawledDate
            #print(item)
            yield item

            # 翻页，点击下一页返回的url
            next_url = response.xpath('//div/div/a/@href').extract()[-1]
            yield response.follow(next_url, callback=self.parse)

