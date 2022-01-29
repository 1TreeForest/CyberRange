# -*- coding: utf-8 -*-
import logging
import random
import time
import requests
import pymysql
from scrapy.spiders import Spider
from siteCrawler.common.searchResultPages import SearchResultPages
from siteCrawler.common.searchEngines import SearchEngineResultSelectors
from scrapy.selector import Selector
import re
from siteCrawler.items import ResultItem


class KeywordSpider(Spider):
    name = 'keywordSpider'
    allowed_domains = ['bing.com', 'google.com', 'baidu.com']
    start_urls = []
    keyword_list = None
    search_engine = None
    url_selector = None
    name_selector = None
    keyword_selector = None

    def __init__(self, keyword='all', se='bing', pages=50, *args, **kwargs):
        super(KeywordSpider, self).__init__(*args, **kwargs)
        if keyword == 'all':  # 用户选择根据数据库中的词库进行搜索
            self.conn = pymysql.Connect(
                host='1.15.220.155',
                # host='localhost',
                port=3306,
                user='test',
                password='991125',
                db='spider',
                charset='UTF8',
            )
            self.cursor = self.conn.cursor()
            sql = 'SELECT keyword FROM `querys`;'
            # 执行
            self.cursor.execute(sql)
            # 提交事务
            self.conn.commit()
            self.keyword_list = self.cursor.fetchall()[:]  # 定义爬取范围
        else:  # 用户制定了一个keyword进行搜索
            self.keyword_list = [(keyword,)]
        self.search_engine = se.lower()
        self.url_selector = SearchEngineResultSelectors[self.search_engine + '_url']
        self.name_selector = SearchEngineResultSelectors[self.search_engine + '_name']
        self.keyword_selector = SearchEngineResultSelectors[self.search_engine + '_keyword']

        for keyword in self.keyword_list:  # 对搜索词列表进行遍历
            flag = True
            page_urls = SearchResultPages(keyword[0], se, int(pages))
            for url in page_urls:
                self.start_urls.append(url)
                if flag:
                    logging.debug(url)
                    flag = False
        random.shuffle(self.start_urls)  # 用以随机排列start_urls，使每次爬取更加随机化
        logging.info('已获取{}个关键词，即将开始进行搜索'.format(len(self.keyword_list)))

    def parse(self, response):
        # 提取页面中的元素
        keyword = Selector(response).xpath(self.keyword_selector).extract()
        names = Selector(response).xpath(self.name_selector)
        urls = Selector(response).xpath(self.url_selector).extract()
        now = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        for i in range(len(urls)):  # 对页面中所有的结果进行处理
            item = ResultItem()
            item['keyword'] = keyword[0]
            item['crawledDate'] = now
            item['aliveDate'] = now
            if self.search_engine == 'baidu':
                item['name'] = ''.join(names[i].xpath('./text() | ./em/text()').extract())  # baidu的标题经过高亮处理，需要进一步提取
                try:
                    resp = requests.get(urls[i], timeout=5)
                except Exception as e:
                    # print(e)
                    logging.warning('{}: {} 网站无法访问，已跳过'.format(item['name'], urls[i]))
                    continue
                item['url'] = resp.url
            elif self.search_engine == 'bing':  # bing的标题经过高亮处理，需要进一步提取
                item['name'] = ''.join(names[i].xpath('./text() | ./strong/text()').extract())
                item['url'] = urls[i]
            elif self.search_engine == 'google':  # 谷歌的结果无需进行额外处理
                item['name'] = names[i]
                item['url'] = urls[i]

            item['domain'] = re.search(r'://(.+?)/', item['url']).group(1)  # 正则匹配提取链接的主要部分，用来判断是否已存在该网站的爬取结果
            yield item
