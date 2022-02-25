import scrapy
from movieCrawler.items import MoviecrawlerItem
import re

class DyttSpider(scrapy.Spider):
    #爬虫名
    name = 'dytt'
    # 允许的域
    allowed_domains = ['dytt8.net']
    # 开始爬取的链接
    start_urls = ['http://www.dytt8.net/html/gndy/dyzz/list_23_1.html']

    def parse(self, response):
        # 定义一个存放item的列表
        items = []
        # 标题列表
        name = response.xpath('//table//b/a/text()').extract()
        # 详情列表
        link = response.xpath('//table//b/a/@href').extract()

        # 遍历列表，将结果存入items
        for i in range(0, len(name)):
            # 实例化一个item类，然后将结果全部存入items
            item = MoviecrawlerItem()
            #提取出的电影名中包含其他信息，如”2012年喜剧《男人如衣服》720p.BD国粤双语中字“，需进一步使用正则匹配出书名号中的电影名
            item['name'] = re.findall('《(.*?)》', name[i])[0]
            # 拼接URL，获取所有电影详情的URL，拼成完整的URL来访问地址
            item['link'] = 'http://www.dytt8.net' + link[i]
            item['site'] = 'http://www.dytt8.net'
            # print(item)
            yield item

            items.append(item)

            # 翻页，从第二页开始
            next_urls = response.xpath('//select[@name="sldd"]/option/@value').extract()[2:]
            for next_url in next_urls:
                yield response.follow(next_url, callback=self.parse)

