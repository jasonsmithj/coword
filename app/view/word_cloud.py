# -*- coding: utf-8 -*-

from app import app
from app.model.search import Search
from app.model.elasticsearch.elasticsearch import ElasticSearch
from app.model.elasticsearch.search_result import SearchResult

import sys
from datetime import datetime
from multiprocessing import Process, Pool

class WordSearch():

    def search(self, words, engine):

        now_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_date = datetime.now().strftime("%Y%m%d%H%M%S")
        search = Search()
        search_result = SearchResult()
        elasticsearch = ElasticSearch()

        if engine == 'google':
            urls = search.google_search(words)
        elif engine == 'google_news':
            urls = search.google_news_search(words)
        else:
            return ('検索エンジン選択エラー')

        if urls == 'NG':
            return ('API使用上限')

        index_names = ['search_result', 'count_search_result', 'original_search_result']

        for index_name in index_names:
            elasticsearch.put_setting(index_name)

        for url in urls:
            Process(target=search_result.save, args=(url,words, engine, now_date, file_date, )).start()

        return ('Success')
