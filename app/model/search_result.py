# -*- coding: utf-8 -*-

from collections import Counter

import sys
from app import app

class SearchResult():

    def original_record(self, index, words, url, engine, body, now_date):
        return {'_index': index, '_type': index, '_source': {'key_word': words, 'url': url, 'engine': engine, 'body': body, 'created_at': now_date }}

    def ma_record(self, index, words, urls, engine, bodys, now_date):
        dic = {'key_word': words, 'url': urls, 'engine': engine}
        s = {}

        for i,body in enumerate(bodys):
            num = '{0:05d}'.format(i)
            s.update({'word_' + str(num): body})

        dic.update({'word': s, 'created_at': now_date})

        return {'_index': index, '_type': index, '_source': dic}

    def count_record(self, index, words, urls, engine, bodys, now_date):
        dic = {'key_word': words, 'url': urls, 'engine': engine}
        noo = {}
        counter = Counter(bodys)
        for word, cnt in counter.most_common():
            noo.update({word:cnt})

        for i,body in enumerate(noo):
            num = '{0:05d}'.format(i)
            dic.update({'word_' + str(num): {'word': body, 'count': noo[body]}})

        dic.update({'created_at': now_date})

        return {'_index': index, '_type': index, '_source': dic}

    def article_original_record(self, index, url, body, now_date):
        return {'_index': index, '_type': index, '_source': {'url': url, 'body': body, 'created_at': now_date }}

    def article_ma_record(self, index, urls, bodys, now_date):
        dic = {'url': urls}
        s = {}

        for i,body in enumerate(bodys):
            num = '{0:05d}'.format(i)
            s.update({'word_' + str(num): body})

        dic.update({'word': s, 'created_at': now_date})

        return {'_index': index, '_type': index, '_source': dic}

    def article_count_record(self, index, urls, bodys, now_date):
        dic = {'url': urls}
        noo = {}
        counter = Counter(bodys)
        for word, cnt in counter.most_common():
            noo.update({word:cnt})

        for i,body in enumerate(noo):
            num = '{0:05d}'.format(i)
            dic.update({'word_' + str(num): {'word': body, 'count': noo[body]}})

        dic.update({'created_at': now_date})

        return {'_index': index, '_type': index, '_source': dic}
