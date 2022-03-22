import logging
import platform
import random

import pymysql
import scrapy
from scrapy_splash import SplashRequest
from time import sleep


class SplashhtmlspiderSpider(scrapy.Spider):
    name = 'homepageHtmlSpider'
    start_urls = []
    count = 0
    save_path = None

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
        sql = 'select domain from domain_homepage where html = 0 order by domain desc'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for item in results:
            self.start_urls.append(item[0])
        self.get_platform()

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url='http://' + url, callback=self.parse, args={'wait': '100'}, endpoint='render.html',
                                meta={'site': url})  # 最大时长、固定参数

    def get_platform(self):
        sysstr = platform.system()
        if sysstr == "Windows":
            self.save_path = '../html/'
        elif sysstr == "Linux":
            self.save_path = '/home/ubuntu/html/'
        else:
            print("Other System tasks")

    def parse(self, response):
        self.save_as_text(response)  # 存为文本格式

        logging.info('已处理 {0} 个页面'.format(self.count))

    def save_as_text(self, response):
        self.count += 1
        with open(self.save_path + 'homepage/{}.html'.format(response.meta.get('site')), 'w',
                  encoding="utf-8") as f:
            try:
                f.write(response.body.decode(encoding='{0}'.format(response.encoding), errors='ignore'))
            except Exception as e:
                print(e)
                sleep(3)
            sql = 'update `domain_homepage` set html = 1 where domain = %s'
            self.cursor.execute(sql, response.meta.get('site'))
            self.conn.commit()
