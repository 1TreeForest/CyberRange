# -*- coding: utf-8 -*-

# Scrapy settings for seCrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'siteCrawler'

SPIDER_MODULES = ['siteCrawler.spiders']

NEWSPIDER_MODULE = 'siteCrawler.spiders'

ITEM_PIPELINES = {'siteCrawler.pipelines.SiteCrawlerPipeline': 1}

DEPTH_LIMIT = 1

LOG_LEVEL = 'INFO'
# CONCURRENT_REQUESTS = 100  # 并发数


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'seCrawler (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN=16
# CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
# COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED=False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    b'Accept': b'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', b'Accept-Language': b'en',
    b'User-Agent': b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    b'Accept-Encoding': b'gzip, deflate'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'siteCrawler.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html

# DOWNLOAD_DELAY = 0.2
RANDOM_DELAY = 3  # 无代理池时设置高延时以防止ban掉IP，random范围是 < 0 ~ RANDOM_DELAY >
DOWNLOADER_MIDDLEWARES = {
    # 'siteCrawler.middlewares.SiteCrawlerDownloaderMiddleware': 543,
    # 'siteCrawler.middlewares.RandomDelayMiddleware': 450,  # 随机延时
    # 'siteCrawler.middlewares.RandomProxyMiddleware': 430,  # 随机代理
    'siteCrawler.middlewares.RandomUserAgentMiddleware': 500,  # 随机UA
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'siteCrawler.pipelines.SomePipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
# AUTOTHROTTLE_ENABLED=True
# The initial download delay
# AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED=True
# HTTPCACHE_EXPIRATION_SECS=0
# HTTPCACHE_DIR='httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES=[]
# HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
