# -*- coding: utf-8 -*-
# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import random
import time
import requests
from scrapy import signals
# from fake_useragent import UserAgent

# class RandomUserAgentMiddleware(object):
#     def process_request(self, request, spider):
#         ua = UserAgent()
#         request.headers['User-Agent'] = ua.random

class SiteCrawlerSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SiteCrawlerDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

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
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomDelayMiddleware(object):
    def __init__(self, delay):
        self.delay = delay

    @classmethod
    def from_crawler(cls, crawler):
        delay = crawler.spider.settings.get("RANDOM_DELAY", 10)
        if not isinstance(delay, int):
            raise ValueError("RANDOM_DELAY need a int")
        return cls(delay)

    def process_request(self, request, spider):
        delay = random.randint(0, self.delay)
        logging.debug("### random delay: %s s ###" % delay)
        time.sleep(delay)


class RandomProxyMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    http_proxy_list = None
    https_proxy_list = None

    def __init__(self):
        self.get_proxy_list()
        self.check_proxy_list()
        logging.info(
            '已成功获取代理池, 代理池余额为:\nhttp:{}\nhttps:{}'.format(len(self.http_proxy_list), len(self.https_proxy_list)))

    def get_proxy_list(self):
        url = 'http://1.15.220.155:5010/all/'
        resp = requests.get(url)
        json = resp.json()
        self.http_proxy_list = [i['proxy'] for i in json if i['https'] is False]
        self.https_proxy_list = [i['proxy'] for i in json if i['https'] is True]

    def check_proxy_list(self):
        url = 'https://www.bing.com/search?q=%E5%85%8D%E8%B4%B9%E7%94%B5%E5%BD%B1&first=20'
        # for proxy in self.http_proxy_list:  # 检查http代理可用性
        #     proxies = {
        #         'http': 'http://' + proxy
        #     }
        #     try:
        #         requests.get(url, proxies=proxies, timeout=5)
        #     except:
        #         self.http_proxy_list.remove(proxy)
        #     logging.info('可用http代理余额:{}'.format(len(self.http_proxy_list)))

        for proxy in self.https_proxy_list:  # 检查https代理可用性
            proxies = {
                'https': 'https://' + proxy
            }
            try:
                resp = requests.get(url, proxies=proxies, timeout=5)
            except:
                self.https_proxy_list.remove(proxy)
                logging.info('可用https代理余额:{}'.format(len(self.https_proxy_list)))

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

        if len(self.http_proxy_list) == 0 or len(self.https_proxy_list) == 0:  # 若代理池为空则重新获取代理池
            self.get_proxy_list()
            self.check_proxy_list()
        if 'baidu' in request.url:
            if request.url.startswith('https://wappass'):  # 访问百度时，若被ban则删除代理池中失效的代理并且重新进行请求
                if request.meta['proxy'].startswith('http://'):
                    if request.meta['proxy'][7:] in self.http_proxy_list:
                        self.http_proxy_list.remove(request.meta['proxy'][7:])
                        logging.warning(
                            '失效代理:{} 已被移除, http代理池余额:{}'.format(request.meta['proxy'], len(self.http_proxy_list)))
                elif request.meta['proxy'].startswith('https://'):
                    if request.meta['proxy'][8:] in self.https_proxy_list:
                        self.https_proxy_list.remove(request.meta['proxy'][8:])
                        logging.warning(
                            '失效代理:{} 已被移除, https代理池余额:{}'.format(request.meta['proxy'], len(self.https_proxy_list)))
                del request.meta['proxy']
                request._set_url(request.meta['redirect_urls'][0])
                del request.meta['redirect_urls']

                if request.url.startswith('http://'):
                    request.meta['proxy'] = 'http://' + random.choice(self.http_proxy_list)
                elif request.url.startswith('https://'):
                    request.meta['proxy'] = 'https://' + random.choice(self.https_proxy_list)

            else:  # 若是正常请求则只设置代理即可
                if request.url.startswith('http://'):
                    request.meta['proxy'] = 'http://' + random.choice(self.http_proxy_list)
                elif request.url.startswith('https://'):
                    request.meta['proxy'] = 'https://' + random.choice(self.https_proxy_list)

        if 'bing' in request.url:
            if request.url.startswith('http://'):
                request.meta['proxy'] = 'http://' + random.choice(self.http_proxy_list)
            elif request.url.startswith('https://'):
                request.meta['proxy'] = 'https://' + random.choice(self.https_proxy_list)


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        return response

    def spider_opened(self, spider):
        spider.logger.info('代理中间件已启用')
