import codecs
# 导入json模块
import json

class SpecificcrawlerPipeline(object):
    # 初始化函数，创建json文件，指定编码格式
    def __init__(self):
        self.filename = codecs.open('dytt.json', 'w', encoding='utf-8')

    # 将item写入，在结尾增加换行符
    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.filename.write(content)
        # 解析一个存一个，返回item继续跟进
        return item

    # 爬问后就把文件关了，释放资源
    def spider_close(self, spider):
        self.filename.close()


# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# import pymysql
# import logging
# from SpecificCrawler.items import ResultItem
# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
#
#
# class SpecificcrawlerPipeline(object):
#     conn = None
#     cursor = None
#     count = None
#
#     def __init__(self):
#         self.db_connect()
#         self.count = 0
#
#     def db_connect(self):
#         self.conn = pymysql.Connect(  # 配置数据库
#             host='1.15.220.155',
#             port=3306,
#             user='test',
#             password='991125',
#             db='spider',
#             charset='UTF8'
#         )
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         try:
#             self.conn.ping(reconnect=True)
#         except Exception as e:
#             self.db_connect()
#             logging.warning("数据库已重新连接")
#
#         # print(item['url']+'\n')
#         # self.file.write(item['url'] + '\n')
#         if isinstance(item, ResultItem):
#             # 拼接insert SQL语句，把每项数据的5个属性填充到SQL中作为参数
#             try:  # 此项在插入时若数据库中已存在该主键对，则进行更新操作
#                 sql = 'INSERT INTO `movies`(name, link, site)VALUES("%s","%s","%s")' % (
#                     item['name'], item['link'], item['site'])
#                 # 执行
#                 self.cursor.execute(sql)
#                 # 提交事务
#                 self.conn.commit()
#                 logging.info('已进行 {} 次数据采集\t\t获取到新对象: {}'.format(self.count, item['domain']))
#             except Exception as e:
#                 sql = 'UPDATE `results` SET name="%s", url="%s", aliveDate="%s" WHERE domain="%s" AND keyword="%s" ' \
#                       % (item['name'], item['url'], item['aliveDate'], item['domain'], item['keyword'])
#                 # 执行
#                 self.cursor.execute(sql)
#                 # 提交事务
#                 self.conn.commit()
#                 logging.info('已进行 {} 次数据采集\t{} 的信息已更新'.format(self.count, item['domain']))
#             self.count += 1
#             # sql = 'select name from `results` where domain="%s" and keyword="%s"' % (item['domain'], item['keyword'])
#             # 执行
#             # self.cursor.execute(sql)
#             # 提交事务
#             # self.conn.commit()
#             print(item)
#
