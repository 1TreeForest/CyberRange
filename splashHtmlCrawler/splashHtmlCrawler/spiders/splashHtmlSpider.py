import pymysql
import scrapy
from scrapy_splash import SplashRequest


class SplashhtmlspiderSpider(scrapy.Spider):
    name = 'splashHtmlSpider'
    start_urls = []
    item_dict = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        conn = pymysql.Connect(  # 配置数据库
            host='1.15.220.155',
            port=3306,
            user='test',
            password='991125',
            db='spider',
            charset='UTF8'
        )
        cursor = conn.cursor()
        # 从数据库中读取需要爬取html的url
        sql = "select url, domain from `results` where isPMS is not null"
        cursor.execute(sql)
        item_list = cursor.fetchall()
        print("读取完成,共需爬取%d个网页" % len(item_list))
        self.item_dict = dict(item_list)  # 将查询结果转为字典，方便存储
        for url in self.item_dict.keys():
            self.start_urls.append(url)
        print(self.start_urls)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': '10'}, endpoint='render.html')  # 最大时长、固定参数

    def parse(self, response):
        with open('../html/{}.html'.format(self.item_dict.get(response.request.url)), 'wb') as f:
            f.write(response.body)
