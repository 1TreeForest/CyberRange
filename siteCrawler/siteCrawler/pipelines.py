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
            host='localhost',
            port=3306,
            user='clwang23',
            password='123456',
            db='mlproj',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.conn.ping(reconnect=True)
        # print(item['url']+'\n')
        # self.file.write(item['url'] + '\n')
        if isinstance(item, ResultItem):
            # 拼接insert SQL语句，把每项数据的5个属性填充到SQL中作为参数
            try:  # 此项在插入时若数据库中已存在该主键对，则进行更新操作
                sql = 'INSERT INTO sites(domain, title, url, keyword, crawledDate, aliveDate)VALUES(%s,%s,%s,%s,%s,%s)'
                # 执行
                self.cursor.execute(sql, [item['domain'], item['name'], item['url'], item['keyword'], item['crawledDate'], item['aliveDate']])
                # 提交事务
                self.conn.commit()
                #sql = 'INSERT IGNORE INTO unmarked(domain, name, url)VALUES(%s,%s,%s)'
                # 执行
                #self.cursor.execute(sql, [item['domain'], item['name'], item['url']])
                # 提交事务
                self.conn.commit()
                logging.info('已进行 {} 次数据采集\t\t获取到新对象: {}'.format(self.count, item['domain']))
            except Exception as e:
                print(e)
                sql = 'UPDATE `sites` SET title=%s, url=%s, aliveDate=%s WHERE domain=%s AND keyword=%s'
                # 执行
                self.cursor.execute(sql, [item['name'], item['url'], item['aliveDate'], item['domain'], item['keyword']])
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
