import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from SpecificCrawler.items import ResultItem

class SpecificSpider(scrapy.Spider):
    #爬虫名
    name = 'Specific'
    #允许的域
    allowed_domains = ['dytt8.net']
    #开始爬取的链接
    start_urls = ['http://www.dytt8.net/html/gndy/dyzz/list_23_1.html']


    def parse(self, response):
        #定义一个存放item的列表
        items = []
        #标题列表
        name = response.xpath('//table//b/a/text()').extract()
        #详情列表
        link = response.xpath('//table//b/a/@href').extract()

        # 遍历列表，将结果存入items
        for i in range(0, len(name)):
            # 实例化一个item类，然后将结果全部存入items
            item = ResultItem()
            item['name'] = name[i]
            # 拼接URL，获取所有电影详情的URL，拼成完整的URL来访问地址
            item['link'] = 'http://www.dytt8.net' + link[i]
            item['site']= 'http://www.dytt8.net'
            print(item)

            items.append(item)

            #翻页，从第二页开始
            next_urls = response.xpath('//select[@name="sldd"]/option/@value').extract()[2:]
            for next_url in next_urls:
                yield response.follow(next_url, callback=self.parse)




        yield item
