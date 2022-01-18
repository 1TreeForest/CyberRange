import scrapy
import pandas as pd  # 导入pandas库
import MySQLdb
import re

from urllib.parse import urlparse

count=0

connect= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='',
        db ='ip',
        )
cursor = connect.cursor()

sql = "select url from results"
cursor.execute(sql)
urls = cursor.fetchall() #取到数据放到data里,返回值是多个元组,即返回多个行记录,
url_list = []
for url in urls:
    url_list.append(url[0])
    count = count + 1

sql = "select domain from results"
cursor.execute(sql)
domains = cursor.fetchall()  # 取数据库中的domain放到name里,便于之后的命名返回值是多个元组,即返回多个行记录
domain_list = []
for domain in domains:
    domain_list.append(domain[0])

cursor.close()
connect.close()

print("写入完成,共写入%d条数据……" % count)

num = 0


class HtmlSpider(scrapy.Spider):
    name = 'html'


    def start_requests(self):
         for url in url_list:
             yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        global num
        filename = '%s.html' % (domain_list[num])
        with open(r"./html/" + filename, 'wb') as f:
            f.write(response.body)
            num = num+1
        self.log('Saved file %s' % filename)




