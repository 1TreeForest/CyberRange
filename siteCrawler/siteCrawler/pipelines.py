# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymysql
from siteCrawler.items import ResultItem


class SiteCrawlerPipeline(object):
    conn = None
    cursor = None
    count = None

    def __init__(self):
        self.db_connect()
        self.count = 0

    def db_connect(self):
        self.conn = pymysql.Connect(  # 配置数据库
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

    def process_item(self, item, spider):
        self.conn.ping(reconnect=True)
        if isinstance(item, ResultItem):
            # 拼接insert SQL语句，把每项数据的5个属性填充到SQL中作为参数
            # 在插入时若数据库中已存在该主键对，则进行更新操作
            sql = 'REPLACE INTO `results`(`domain`, `name`, `url`, `keyword`, `crawledDate`, `aliveDate`) VALUES("{}","{}","{}","{}","{}","{}");'.format(
                item['domain'], item['name'], item['url'], item['keyword'], item['crawledDate'], item['aliveDate'])
            # 执行
            affected_rows = self.cursor.execute(sql)
            print('{}\n{}'.format(sql, affected_rows))
            # 提交事务
            # self.conn.commit()
            logging.info('已进行 {} 次数据采集'.format(self.count))
            self.count += 1
            print(item)
