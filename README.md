# CyberRange

## SiteCrawler

### 根据数据库中的词表批量运行



### 手动输入参数运行

进入siteCrawler目录后运行如下命令

#### Bing
```scrapy crawl keywordSpider -a keyword=Spider-Man -a se=bing -a pages=50```

#### Baidu
```scrapy crawl keywordSpider -a keyword=Spider-Man -a se=baidu -a pages=50```

#### Google
```scrapy crawl keywordSpider -a keyword=Spider-Man -a se=google -a pages=50```