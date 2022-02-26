import logging
import random

import pymysql
import scrapy
import re

from movieCrawler.items import UniversalItem


class UniversalSpider(scrapy.Spider):
    conn = None
    cursor = None
    item_list = []
    name = 'universalSpider'
    #  黑名单短语列表，若出现在name中则剔除
    black_word_list = ['最新', 'topics', '会员', 'vip', 'VIP', '围观了', '点击图标', '分享到', '客户端', '热线', 'rss', 'RSS', '排行榜', '留言', '电影大全', '？？', '??']
    #  黑名单题目列表，若与提取所得title相等则剔除
    black_title_list = ['招聘英才', '联系我们', '关于我们', '', ]
    #  黑名单url列表，若与提取所得link相等则剔除
    black_link_list = ['javascript::', '#', '']
    start_urls = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = pymysql.Connect(
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
        sql = 'SELECT url, domain FROM `pms`'
        # 执行
        self.cursor.execute(sql)
        # 提交事务
        self.conn.commit()
        self.item_list = dict(self.cursor.fetchall()[:])  # 定义爬取范围
        for url in self.item_list.keys():
            self.start_urls.append(url)
        logging.info('通用资源爬虫已获取 {} 个url，即将开始进行爬取'.format(len(self.item_list)))
        random.shuffle(self.start_urls)  # 用以随机排列start_urls，使每次爬取更加随机化
        print(self.start_urls)

    def parse(self, response):
        tag_list = response.selector.xpath('//*[@title]')  # 提取所有含title属性的tag，用以解析其中内容
        site_url = response.request.url
        item = UniversalItem()
        for tag in tag_list:
            try:
                title = tag.xpath('./@title').extract()[0]
                href = tag.xpath('./@href').extract()[0]
                if not href.startswith('http'):  # 处理本站内数据，即站内数据要加上前缀url
                    if href[0] == '/' and site_url[-1] == '/':
                        href = site_url + href[1:]
                    elif href[0] == '/' and site_url[-1] != '/' or href[0] != '/' and site_url[-1] == '/':
                        href = site_url + href
                    elif href[0] != '/' and site_url[-1] != '/':
                        href = site_url + '/' + href
                    else:
                        print('error!\n{}'.format(title, '\t', href, '\t', '*' * 100))
                # title_in_brackets = re.search(r'《(.+?)》', title).group(1)  # 去除书名号，慎用
                # if title_in_brackets:
                #     title = title_in_brackets
                item['link'] = href
                item['name'] = title
                item['site'] = self.item_list.get(site_url)
                # print(item)

                if any(word in item['name'] for word in self.black_word_list) or any(
                        title == item['name'] for title in self.black_title_list) or any(
                        url == item['link'] for url in self.black_link_list):  # 若不符合三个黑名单所定义的规则就剔除
                    continue

                yield item
                # print(item)

            except Exception as e:
                continue
