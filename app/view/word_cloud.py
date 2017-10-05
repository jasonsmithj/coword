# -*- coding: utf-8 -*-

from app import app
from app.model.search import Search
from app.model.morphological_analysis import MorphologicalAnalysis
from app.model.search_result import SearchResult
from app.model.elasticsearch import ElasticSearch

import sys
from datetime import datetime
from multiprocessing import Pool

class WordSearch():

    def search(self, words, engine):

        now_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        search = Search()
        morphological_analysis = MorphologicalAnalysis()
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

        actions = []
        count_actions = []
        original_actions = []
        for i,url in enumerate(urls):
            body = search.scraping(url)
            original_actions.append(search_result.original_record('original_search_result', words, url, engine, body, now_date))
            key_word = morphological_analysis.parse(body)
            actions.append(search_result.ma_record('search_result', words, url, engine, key_word, now_date))
            count_actions.append(search_result.count_record('count_search_result', words, url, engine, key_word, now_date))

            if i % 10 == 0 :
                try:
                    for action in [actions, count_actions, original_actions]:
                        elasticsearch.save(action)
                except Exception as e:
                    app.logger.error(e.args)
                    return (e.args)
                else:
                    actions = []
                    count_actions = []
                    original_actions = []
        return ('Success')
