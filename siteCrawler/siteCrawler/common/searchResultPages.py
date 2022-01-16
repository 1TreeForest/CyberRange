# -*- coding: utf-8 -*-
from .searchEngines import SearchEngines


class SearchResultPages:
    total_page = 0
    keyword = None
    search_engine_url = None
    current_page = 0
    search_engine = None

    def __init__(self, keyword, search_engine, total_page):  # 根据用户输入配置keyword和engine、爬取页数
        self.search_engine = search_engine.lower()
        self.search_engine_url = SearchEngines[self.search_engine]
        self.total_page = total_page
        self.keyword = keyword
        print("total page:{0}".format(self.total_page))

    def __iter__(self):
        return self

    def _current_url(self):
        return self.search_engine_url.format(self.keyword, str(self.current_page * 10))

    def __next__(self):
        if self.current_page < self.total_page:
            url = self._current_url()
            self.current_page = self.current_page + 1
            return url
        raise StopIteration
