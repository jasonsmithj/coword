# -*- coding: utf-8 -*-

from app import app
from app.model.search import Search
from app.model.search_result import SearchResult
from app.model.morphological_analysis import MorphologicalAnalysis

import json

class SearchResult():

    def save(self, url, words, engine, now_date, file_date):
        search = Search()
        search_result = SearchResult()
        morphological_analysis = MorphologicalAnalysis()

        body = search.scraping(url)
        key_word = morphological_analysis.parse(body)
        app.logger.info(search_result.original_record('original_search_result', words, url, engine, body, now_date))

        with open(app.config['TMP_PATH'] + 'search_result_' + file_date + '.json', "a") as f:
            f.write(json.dumps(search_result.ma_record('search_result', words,  url, engine, key_word, now_date)))
            f.write('\n')

        with open(app.config['TMP_PATH'] + 'original_search_result_' + file_date + '.json', "a") as f:
            f.write(json.dumps(search_result.original_record('original_search_result', words, url, engine, body, now_date)))
            f.write('\n')

        with open(app.config['TMP_PATH'] + 'count_search_result_' + file_date + '.json', "a") as f:
            f.write(json.dumps(search_result.count_record('count_search_result', words, url, engine, key_word, now_date)))
            f.write('\n')

