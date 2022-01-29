# -*- coding: utf-8 -*-
from scrapy import cmdline

cmdline.execute("scrapy crawl keywordSpider -a keyword=all -a se=bing -a pages=20".split())
