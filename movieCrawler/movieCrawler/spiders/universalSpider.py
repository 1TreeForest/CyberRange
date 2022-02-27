import logging
import random
from time import sleep

import pymysql
import scrapy
import re
from scrapy_splash import SplashRequest

from movieCrawler.items import UniversalItem


class UniversalSpider(scrapy.Spider):
    conn = None
    cursor = None
    item_list = []
    name = 'universalSpider'
    #  黑名单短语列表，若出现在name中则剔除
    black_word_list = ['topics', '会员', 'vip', 'VIP', '围观了', '点击图标', '分享到', '客户端', '热线', 'rss', 'RSS',
                       '排行榜', '留言', '大全', '？？', '??', '频道', '站点地图', '跳转', '类型的电影', '话题', 'QQ', 'qq',
                       ]
    #  黑名单题目列表，若与提取所得title相等则剔除
    black_title_list = ['招聘英才', '联系我们', '关于我们', '', '首页', '观看历史', '播放记录', '资讯', '分享', '评论', '生活',
                        '电影', '少儿', '剧情', '动作', '歌舞', '冒险', '惊悚', '悬疑', '剧情', '喜剧', '科幻', '爱情']
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

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': '3'}, endpoint='render.html')  # 最大时长、固定参数

    def parse(self, response):
        tag_list = response.selector.xpath('//*[@title]')  # 提取所有含title属性的tag，用以解析其中内容
        site_url = response.request.url
        item = UniversalItem()
        for tag in tag_list:
            title = tag.xpath('./@title').extract()[0]
            href = tag.xpath('./@href').extract()[0]
            if not href.startswith('http'):  # 处理本站内数据，即站内数据要加上前缀url
                if href[0] == '/' and site_url[-1] == '/':
                    href = site_url + href[1:]
                elif href[0] == '/' and site_url[-1] != '/' or href[0] != '/' and site_url[-1] == '/':
                    href = site_url + href
                elif href[0] != '/' and site_url[-1] != '/':
                    href = site_url + '/' + href
            # title_in_brackets = re.search(r'《(.+?)》', title).group(1)  # 去除书名号，慎用
            # if title_in_brackets:
            #     title = title_in_brackets
            item['link'] = href
            item['name'] = title
            item['site'] = self.item_list.get(site_url)
            # print(item)

            if any(word in item['name'] for word in self.black_word_list) or \
                    any(title == item['name'] for title in self.black_title_list) or \
                    any(url == item['link'] for url in self.black_link_list or
                    item['name'].isalnum()):  # 若不符合三个黑名单所定义的规则就剔除
                # sql = 'insert ignore into `black_log` value("%s")' % item['name']
                # self.cursor.execute(sql)
                # self.conn.commit()
                continue

            yield item
            # print(item)