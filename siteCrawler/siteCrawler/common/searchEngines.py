# -*- coding: utf-8 -*-

SearchEngines = {  # 记录搜索站及搜索url格式
    'google': 'https://www.google.com/search?q={0}&start={1}',
    'bing': 'https://www.bing.com/search?q={0}&first={1}',
    'baidu': 'https://www.baidu.com/s?wd={0}&pn={1}'
}

SearchEngineResultSelectors = {  # 记录xpath提取不同的元素
    'google_url': '//h3/a/@href',
    'google_name': '//h3/a/text()',
    'google_keyword': '//*[@id="tsf"]/div[1]/div[1]/div[2]/div[1]/div/div[2]/input/@value',
    'bing_url': '//h2/a/@href',
    'bing_name': '//h2/a',
    'bing_keyword': '//*[@id="sb_form_q"]/@value',
    'baidu_url': '//h3/a/@href',
    'baidu_name': '//h3/a',
    'baidu_keyword': '//*[@id="kw"]/@value',
}
