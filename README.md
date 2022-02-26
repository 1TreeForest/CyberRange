# CyberRange
## 目录结构
/CyberRange  

|-- splashHtmlCrawler/    
|   |-- html/  #保存对URL进行爬取后得到的经过渲染的HTML文件    
|   |-- splashHtmlCrawler/ #爬虫文件
|   |-- scrapy.cfg  

|-- siteCrawler/   
|   |-- siteCrawler/   
|   |-- scrapy.cfg   

|-- movieCrawler/   
|   |-- movieCrawler/   
|   |   |--spider/  
|   |   |  |--dytt.py #爬取电影天堂网站上信息的爬虫  
|   |   |  |--movie——2345.py #爬取2345电影网站上信息的爬虫  
|   |   |  |--universalSpider.py #爬取所有侵权网站上信息的普适性爬虫  
|   |-- scrapy.cfg   

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



## htmlCrawler
### 更改数据库配置
在htmlSpider.py中的coonect中配置数据库连接的参数
### 手动输入参数运行

进入htmlCrawler目录后运行如下命令
```scrapy crawl html```  

## movieCrawler
### universalSpider.py
运行run_universal.py文件开启爬虫
### movie_2345.py、 dytt.py
运行run_special.py文件开启爬虫



