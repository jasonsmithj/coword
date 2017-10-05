# -*- coding: utf-8 -*-

from app import app
from collections import Counter
import csv
import glob
import json
import re

class Report():

    def create_report(self, data):
        def int_chk(my_str):
            regex = r'[0-9]+'
            str_match = re.compile(regex).fullmatch(str(my_str))
            if str_match == None:
                raise ValueError("{} cannot cast intger".format(str(my_str)))

        corpus_length = len(data['hits']['hits'])
        count_data = {}

        for i in range(corpus_length):
            corpus_data = data['hits']['hits'][i]['_source']
            corpus_data = corpus_data.values()
            for word_count in corpus_data:
                try:
                    int_chk(word_count['count'])
                except ValueError as e:
                    app.logger.error(e)
                else:
                    count_data[word_count['word']] = count_data.get(word_count['word'], 0) + int(word_count['count'])

        return sorted(count_data.items(), key=lambda x: x[1], reverse=True)

    def article_count(self, data):
        return (str(data['hits']['total']))
