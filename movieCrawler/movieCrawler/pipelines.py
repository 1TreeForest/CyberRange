import json
import pymysql
from movieCrawler.items import MoviecrawlerItem
import codecs
import logging

# 导入json模块
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MoviecrawlerPipeline(object):
    conn = None
    cursor = None
    count = None

    def __init__(self):
        self.db_connect()
        self.count = 0

    def db_connect(self):
        self.conn = pymysql.Connect(  # 配置数据库
            host='1.15.220.155',
            port=3306,
            user='test',
            password='991125',
            db='spider',
            charset='UTF8'
        )
        self.cursor = self.conn.cursor()

    # 将item写入，在结尾增加换行符
    def process_item(self, item, spider):
        try:
            self.conn.ping(reconnect=True)
        except Exception as e:
            self.db_connect()
            logging.warning("数据库已重新连接")

            # 拼接insert SQL语句
            sql = 'INSERT INTO `movies`(name, link, site)VALUES("%s","%s","%s")' % (
                item['name'], item['link'], item['site'])
            # 执行
            self.cursor.execute(sql)
            # 提交事务
            self.conn.commit()
            logging.info('已进行 {} 次数据采集\t\t获取到新对象: {}，{}'.format(self.count, item['name'], item['link']))
            self.count += 1
            print(item)

        # content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        # self.filename.write(content)
        # # 解析一个存一个，返回item继续跟进
        # return item

    # # 爬问后就把文件关了，释放资源
    # def spider_close(self, spider):
    #     self.filename.close()

