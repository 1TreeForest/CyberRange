import logging
import random
from time import sleep

import pymysql
import scrapy
import re
from scrapy_splash import SplashRequest

from movieCrawler.items import UniversalItem, FriendLinkItem


class UniversalSpider(scrapy.Spider):
    conn = None
    cursor = None
    item_dict = []
    name = 'universalSpider'
    #  黑名单短语列表，若出现在name中则剔除
    black_word_list = ['topics', '会员', 'vip', 'VIP', '围观了', '点击图标', '分享到', '客户端', '热线', 'rss', 'RSS',
                       '排行榜', '留言', '大全', '？？', '??', '频道', '地图', '跳转', '类型的电影', '话题', 'QQ', 'qq',
                       '直达', 'google', 'baidu', 'bing', 'sogou']
    #  黑名单题目列表，若与提取所得title相等则剔除
    black_title_list = ['招聘英才', '联系我们', '关于我们', '', '首页', '观看历史', '播放记录', '资讯', '分享', '评论', '生活',
                        '电影', '少儿', '剧情', '动作', '歌舞', '冒险', '惊悚', '悬疑', '剧情', '喜剧', '科幻', '爱情', '上一页', '下一页', '\n',
                        '\t']
    #  黑名单url列表，若与提取所得link相等则剔除
    black_link_list = ['#', '']
    black_link_word_list = ['javascript']
    start_urls = []
    last_name = None
    last_page = None

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
        self.item_dict = dict(self.cursor.fetchall()[:])  # 定义爬取范围
        for url in self.item_dict.keys():
            self.start_urls.append(url)
        logging.info('通用资源爬虫已获取 {} 个url，即将开始进行爬取'.format(len(self.item_dict)))
        random.shuffle(self.start_urls)  # 用以随机排列start_urls，使每次爬取更加随机化
        print(self.start_urls)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': '10'}, endpoint='render.html',
                                meta={'original_url': url})  # 最大时长、固定参数

    def parse(self, response):
        tag_list = response.selector.xpath('//*[@title]')  # 提取所有含title属性的tag，用以解析其中内容
        site_url = response.meta.get('original_url')
        item = UniversalItem()
        for tag in tag_list:
            try:
                href = tag.xpath('./@href').extract()[0]
                title = tag.xpath('./@title').extract()[0]
            except:
                continue
            if title == self.last_name:
                continue
            if not href.startswith('http'):  # 处理本站内数据，即站内数据要加上前缀url
                if href.startswith('/'):
                    pre = re.search(r'https?://.+?/', response.url).group(0)  # 匹配最短路径
                    href = pre + href[1:]
                else:
                    pre = re.search(r'https?://.+/', response.url).group(0)  # 匹配最长路径
                    href = pre + href
            # title_in_brackets = re.search(r'《(.+?)》', title).group(1)  # 去除书名号，慎用
            # if title_in_brackets:
            #     title = title_in_brackets
            item['link'] = href
            item['name'] = title
            item['site'] = self.item_dict.get(site_url)
            # print(item)

            if any(word in item['name'] for word in self.black_word_list) or \
                    any(title == item['name'] for title in self.black_title_list) or \
                    any(url == item['link'] for url in self.black_link_list) or \
                    any(url in item['link'] for url in self.black_link_word_list) or \
                    item['name'].isalnum():  # 若不符合四个黑名单所定义的规则就剔除
                sql = 'insert ignore into `black_log` value("%s")' % item['name']
                self.cursor.execute(sql)
                self.conn.commit()
                continue
            yield item
            self.last_name = title

        yield from self.get_friend_link_and_next_page(response)  # 提取友情链接以及爬取下一页

    def get_friend_link_and_next_page(self, response):
        link_list = response.selector.xpath('//*[@href]')  # 提取所有含href属性的tag，用以解析其中内容
        site_url = response.meta.get('original_url')
        for link in link_list[:]:
            href = link.xpath('./@href').extract()[0]
            try:
                name = link.xpath('./@title').extract()[0]
            except:
                name = link.xpath('./text()').extract()
                try:
                    name = name[0]
                except:
                    continue
            if not href.startswith('http'):  # 如果是站内链接，证明可能为下一页的链接
                if '下一页' in name:
                    print('处理下一页')
                    if 'javascript' in href:
                        continue
                    if href.startswith('/'):
                        pre = re.search(r'https?://.+?/', response.url).group(0)
                        href = pre + href[1:]
                    else:
                        pre = re.search(r'https?://.+/', response.url).group(0)
                        href = pre + href
                    if href == self.last_page:
                        print('此网站已爬取所有页数', '\t', href)
                        continue
                    yield SplashRequest(url=href, callback=self.parse, args={'wait': '10'}, endpoint='render.html',
                                        meta={'original_url': site_url})  # 最大时长、固定参数
                    print(href)
                    print('下一页处理成功')
                    self.last_page = href
                    continue
            elif href.startswith('http'):  # 处理友情链接
                friend_link_item = FriendLinkItem()
                friend_link_item['name'] = name
                friend_link_item['link'] = href
                try:
                    friend_link_item['domain'] = re.search(r'://(.+?)[:/]?', href).group(
                        1)  # 正则匹配提取链接的主要部分，用来判断是否已存在该网站的爬取结果
                except:
                    print(href)
                    continue
                if any(word in friend_link_item['name'] for word in self.black_word_list) or \
                        any(title == friend_link_item['name'] for title in self.black_title_list) or \
                        any(url == friend_link_item['link'] for url in self.black_link_list) or \
                        any(url in friend_link_item['link'] for url in self.black_link_word_list) or \
                        friend_link_item['name'].isalnum():  # 若不符合四个黑名单所定义的规则就剔除
                    continue
                yield friend_link_item
