import scrapy
import pandas as pd  # 导入pandas库
from sqlalchemy import create_engine  # 导入create_engine函数
import MySQLdb
import re

connect= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='',
        db ='test',
        )
cursor = connect.cursor()

sql = "select url from testtable"
cursor.execute(sql)
data = cursor.fetchall() #取到数据放到data里,返回值是多个元组,即返回多个行记录,
count = 0
url_list = []

for url in data:
    url_list.append(url[0])
    count = count + 1

cursor.close()
connect.close()
print("写入完成,共写入%d条数据……" % count)
print(url_list)
for url in url_list:
    print(url)

page = 0

class HtmlSpider(scrapy.Spider):
    name = 'html'
    page = 0

    def start_requests(self):
         for url in url_list:
             yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        global page
        filename = '%s.html' % (page)
        with open(r"./html/" + filename, 'wb') as f:
            f.write(response.body)
            page = page+1
        self.log('Saved file %s' % filename)




