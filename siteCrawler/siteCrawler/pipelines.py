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
        self.count = 1

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

    def process_item(self, item, spider):
        self.conn.ping(reconnect=True)
        # print(item['url']+'\n')
        # self.file.write(item['url'] + '\n')
        if isinstance(item, ResultItem):
            # 拼接insert SQL语句，把每项数据的5个属性填充到SQL中作为参数
            try:  # 此项在插入时若数据库中已存在该主键对，则进行更新操作
                sql = 'INSERT INTO results(domain, name, url, keyword, crawledDate, aliveDate)VALUES("%s","%s","%s","%s","%s", "%s")' % (
                    item['domain'], item['name'], item['url'], item['keyword'], item['crawledDate'], item['aliveDate'])
                # 执行
                self.cursor.execute(sql)
                # 提交事务
                self.conn.commit()
                logging.info('已进行 {} 次数据采集\t\t获取到新对象: {}'.format(self.count, item['domain']))
            except Exception as e:
                sql = 'UPDATE results SET name="%s", url="%s", aliveDate="%s" WHERE domain="%s" AND keyword="%s"' \
                      % (item['name'], item['url'], item['aliveDate'], item['domain'], item['keyword'])
                # 执行
                self.cursor.execute(sql)
                # 提交事务
                self.conn.commit()
                logging.info('已进行 {} 次数据采集\t{} 的信息已更新'.format(self.count, item['domain']))
            self.count += 1
            # sql = 'select name from `results` where domain="%s" and keyword="%s"' % (item['domain'], item['keyword'])
            # 执行
            # self.cursor.execute(sql)
            # 提交事务
            # self.conn.commit()
            # print(item)
