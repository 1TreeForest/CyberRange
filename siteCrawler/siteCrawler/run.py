# -*- coding: utf-8 -*-
from scrapy import cmdline

cmdline.execute("scrapy crawl keywordSpider_baidu -a keyword=all -a se=baidu -a pages=200".split())
