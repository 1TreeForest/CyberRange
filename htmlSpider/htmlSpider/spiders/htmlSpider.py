import scrapy
import pandas as pd  # 导入pandas库
import MySQLdb
import re
import pymysql

from urllib.parse import urlparse

class HtmlSpider(scrapy.Spider):
    name = 'html'
    num = 0
    url_list = []
    domain_list = []


    def start_requests(self):
        conn = pymysql.Connect(  # 配置数据库
            host='localhost',
            port=3306,
            user='test',
            password='991125',
            db='spider',
            charset='UTF8'
        )
        cursor = conn.cursor()
        #从数据库中读取需要爬取html的url
        sql = "select url from results"
        cursor.execute(sql)
        urls = cursor.fetchall()
        count = 0 #便于记录从数据库中读到多少条url
        for url in urls: # 将取出的url放入url_list里
            self.url_list.append(url[0])
            count = count + 1
        print("写入完成,共写入%d条数据……" % count)

        # 从数据库中读取给html文件命名需要的domain
        sql = "select domain from results"
        cursor.execute(sql)
        domains = cursor.fetchall()
        for domain in domains:  # 将取出的domain放入domain_list里
            self.domain_list.append(domain[0])

        cursor.close()

        #对url_list中的url依次爬取
        for url in self.url_list:
             yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        filename = '%s.html' % (self.domain_list[self.num]) #利用domian命名html文件
        with open(r"./html/" + filename, 'wb') as f:  #html文件保存在html目录下
            f.write(response.body) #将返回的html保存到html文件
            self.num = self.num+1
        self.log('Saved file %s' % filename)




