import logging

import pymysql
import scrapy

from movieCrawler.items import MoviecrawlerItem


class UniversalSpider(scrapy.Spider):
    conn = None
    cursor = None
    name = 'universalSpider'
    start_urls = []
    url_list = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = pymysql.Connect(
            host='1.15.220.155',
            # host='localhost',
            port=3306,
            user='test',
            password='991125',
            db='spider',
            charset='UTF8',
            autocommit=True
        )
        self.cursor = self.conn.cursor()
        sql = 'SELECT url FROM `pms`'
        # 执行
        self.cursor.execute(sql)
        # 提交事务
        self.conn.commit()
        self.url_list = self.cursor.fetchall()[:]  # 定义爬取范围
        for url in self.url_list:
            self.start_urls.append(url[0])
        logging.info('通用资源爬虫已获取{}个url，即将开始进行爬取'.format(len(self.url_list)))
        print(self.start_urls)


    def parse(self, response):
        tag_list = response.selector.xpath('//*[@title]')  # 提取所有含title属性的tag，用以解析其中内容
        site_url = response.url
        for tag in tag_list:
            try:
                title = tag.xpath('./@title').extract()[0]
                href = tag.xpath('./@href').extract()[0]
                item = MoviecrawlerItem()
                if href.startswith('/'):  # 处理本站内数据，即站内数据要加上前缀url
                    href = site_url[:-1] + href
                item['link'] = href
                item['name'] = title
                item['site'] = site_url
                yield item
            except Exception as e:
                print(e)


