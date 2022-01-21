import random

import requests
from requests import Request
from scrapy import signals


class ProxyMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    http_proxy_list = None
    https_proxy_list = None

    def __init__(self):
        url = 'http://1.15.220.155:5010/all/'
        resp = requests.get(url)
        json = resp.json()
        self.http_proxy_list = [i['proxy'] for i in json if i['https'] is False]
        self.https_proxy_list = [i['proxy'] for i in json if i['https'] is True]

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        if request.url.startwith('http://'):
            pass
        elif request.url.startwith('https://'):
            pass
        return None


test = ProxyMiddleware()
print(test.http_proxy_list)
print(test.https_proxy_list)
a = 0
b = 0
for i in test.https_proxy_list:
    try:
        resp = requests.get(url='https://www.google.com/',
                            proxies={'https': 'https://' + i}, timeout=3)

        if 'wappassssssssss' in resp.url:
            print('*'*10, resp.url)
            b += 1
        else:
            print(resp.url)
            a += 1
    except:
        print('*'*10)
        b += 1
print(a, b)
