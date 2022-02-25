# -*- coding: utf-8 -*-
from scrapy import cmdline

cmdline.execute("scrapy crawl keywordSpider -a keyword=all -a se=bing_global -a pages=200".split())
