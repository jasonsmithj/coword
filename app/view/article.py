# -*- coding: utf-8 -*-

from app import app
from app.model.search import Search
from app.model.morphological_analysis import MorphologicalAnalysis
from app.model.search_result import SearchResult
from app.model.csv_to_url import CsvToUrl
from app.model.elasticsearch.elasticsearch import ElasticSearch

import os
import sys
from datetime import datetime

class Article():

    def csv_to_url(self , filename):
        csv = CsvToUrl()
        return (csv.get_url(filename))

    def create_record(self, urls):
        now_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        morphological_analysis = MorphologicalAnalysis()
        search = Search()
        search_result = SearchResult()
        elasticsearch = ElasticSearch()
        engine = 'article'

        index_names = ['article_result', 'count_article_result', 'original_article_result']

        for index_name in index_names:
            elasticsearch.put_setting(index_name)

        actions = []
        count_actions = []
        original_actions = []
        for i,url in enumerate(urls):
            body = search.scraping(url)

            original_actions.append(search_result.article_original_record('original_article_result',  url,  body, now_date))
            key_word = morphological_analysis.parse(body)
            actions.append(search_result.article_ma_record('article_result',  url, key_word, now_date))
            count_actions.append(search_result.article_count_record('count_article_result',  url,  key_word, now_date))

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

    def delete_file(self, filename):
        try:
            os.remove(filename)
        except Exception as e:
            app.logger.error(e)

