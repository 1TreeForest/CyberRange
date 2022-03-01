import logging
import random

import pymysql
import scrapy
from scrapy_splash import SplashRequest
from time import sleep


class SplashhtmlspiderSpider(scrapy.Spider):
    name = 'splashHtmlSpider'
    start_urls = []
    item_dict = {}
    count = 0
    pms_count = 0  # 用来记录有多少条pms记录，用以分两个文件夹存储pms和notpms的网站
    conn = None
    cursor = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = pymysql.Connect(  # 配置数据库
            host='1.15.220.155',
            port=3306,
            user='test',
            password='991125',
            db='spider',
            charset='UTF8'
        )
        self.cursor = self.conn.cursor()
        # 从数据库中读取需要爬取html的url

        #  以下获取方法二选一
        # item_list = self.get_marked_pages()
        item_list = self.get_unmarked_pages()

        self.item_dict = dict(item_list)  # 将查询结果转为字典，方便存储
        for item in item_list:
            self.start_urls.append(item[0])
        print(self.start_urls)

    def get_unmarked_pages(self):
        sql = "select url, domain from `results` where isPMS is null limit 2000"  # 若要整体重爬，注释掉where子句
        self.cursor.execute(sql)
        item_list = self.cursor.fetchall()
        return item_list

    def get_marked_pages(self):
        sql = "select url, domain from `pms` where html = 0"  # 若要整体重爬，注释掉where子句
        self.cursor.execute(sql)
        item_list = self.cursor.fetchall()
        self.pms_count = len(item_list)
        sql = "select url, domain from `notpms` where html = 0"  # 若要整体重爬，注释掉where子句
        self.cursor.execute(sql)
        item_list += self.cursor.fetchall()
        print("读取完成,共需爬取%d个网页" % len(item_list))
        return item_list

    def start_requests(self):
        if self.pms_count == 0:
            for url in self.start_urls[:]:  # 处理unmarked
                yield SplashRequest(url=url, callback=self.parse, args={'wait': '100'}, endpoint='render.html', meta={'site': url, 'flag': 'unmarked'})  # 最大时长、固定参数
        else:
            for url in self.start_urls[:self.pms_count]:  # 处理pms
                yield SplashRequest(url=url, callback=self.parse, args={'wait': '100'}, endpoint='render.html', meta={'site': url, 'flag': 'pms'})  # 最大时长、固定参数
            for url in self.start_urls[self.pms_count:]:  # 处理notpms
                yield SplashRequest(url=url, callback=self.parse, args={'wait': '100'}, endpoint='render.html', meta={'site': url, 'flag': 'notpms'})  # 最大时长、固定参数

    def parse(self, response):
        self.count += 1
        # self.save_as_bin(response)  # 存为二进制格式
        self.save_as_text(response)  # 存为文本格式

        logging.info('已处理 {0} 个页面'.format(self.count))

    def save_as_text(self, response):
        if response.meta.get('flag') == 'unmarked':
            sql = 'update `pms` set html = 1 where url = "%s"' % response.meta.get('site')
            self.cursor.execute(sql)
            self.conn.commit()
            with open('../html/unmarked/{}.html'.format(self.item_dict.get(response.meta.get('site'))), 'w',
                      encoding="utf-8") as f:
                try:
                    f.write(response.body.decode(encoding='{0}'.format(response.encoding), errors='ignore'))
                except Exception as e:
                    print(e)
                    sleep(3)
        elif response.meta.get('flag') == 'pms':
            sql = 'update `pms` set html = 1 where url = "%s"' % response.meta.get('site')
            self.cursor.execute(sql)
            self.conn.commit()
            with open('../html/pms/{}.html'.format(self.item_dict.get(response.meta.get('site'))), 'w',
                      encoding="utf-8") as f:
                try:
                    f.write(response.body.decode(encoding='{0}'.format(response.encoding), errors='ignore'))
                except Exception as e:
                    print(e)
                    sleep(3)
        elif response.meta.get('flag') == 'notpms':
            sql = 'update `notpms` set html = 1 where url = "%s"' % response.meta.get('site')
            self.cursor.execute(sql)
            self.conn.commit()
            with open('../html/notpms/{}.html'.format(self.item_dict.get(response.meta.get('site'))), 'w',
                      encoding="utf-8") as f:
                try:
                    f.write(response.body.decode(encoding='{0}'.format(response.encoding), errors='ignore'))
                except Exception as e:
                    print(e)
                    sleep(3)

    def save_as_bin(self, response):
        if response.meta.get('flag') == 'pms':
            sql = 'update `pms` set html = 1 where url = "%s"' % response.meta.get('site')
            self.cursor.execute(sql)
            self.conn.commit()
            with open('../html/pms/{}.html'.format(self.item_dict.get(response.meta.get('site'))), 'wb') as f:
                f.write(response.body)
        elif response.meta.get('flag') == 'notpms':
            sql = 'update `notpms` set html = 1 where url = "%s"' % response.meta.get('site')
            self.cursor.execute(sql)
            self.conn.commit()
            with open('../html/notpms/{}.html'.format(self.item_dict.get(response.meta.get('site'))), 'wb') as f:
                f.write(response.body)
