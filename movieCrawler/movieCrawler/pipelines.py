import json
import pymysql
from movieCrawler.items import SpecialItem, UniversalItem, FriendLinkItem
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
        if isinstance(item, SpecialItem):
            sql = 'INSERT INTO `movies_special`(name, link, site)VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE link = %s'
            # 执行
            self.cursor.execute(sql, [item['name'], item['link'], item['site'], item['link']])
            # 提交事务
            self.conn.commit()
            logging.info('已进行 {} 次数据采集\t\t获取到对象: {}，{}'.format(self.count, item['name'], item['link']))
            self.count += 1
        if isinstance(item, UniversalItem):
            sql = 'INSERT INTO `movies_universal`(name, link, site)VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE link = %s'
            # 执行
            self.cursor.execute(sql, [item['name'], item['link'], item['site'], item['link']])
            # 提交事务
            self.conn.commit()
            logging.info('已进行 {} 次数据采集\t\t获取到对象: {}，{}，{}'.format(self.count, item['name'], item['link'], item['site']))
            self.count += 1
        # print(item)
        if isinstance(item, FriendLinkItem):
            sql = 'INSERT IGNORE INTO `friend_link`(name, link, domain)VALUES(%s,%s,%s)'
            # 执行
            self.cursor.execute(sql, [item['name'], item['link'], item['domain']])
            # 提交事务
            self.conn.commit()

        # content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        # self.filename.write(content)
        # # 解析一个存一个，返回item继续跟进
        # return item

    # # 爬问后就把文件关了，释放资源
    # def spider_close(self, spider):
    #     self.filename.close()

