# -*- coding: utf-8 -*-

from app import app
from app.model.search import Search
from app.model.elasticsearch import ElasticSearch
from app.model.report import Report
from app.model.file import File

import re

class Reports():

    def create(self, searchword, engine, starttime, endtime, index):
        es = ElasticSearch()
        reports = Report()
        files = File()

        body = es.search(searchword, engine, starttime, endtime, index)

        search_engine = ','.join(engine)
        headers = ('検索エンジン : ' + str(search_engine).lstrip('[\'').rstrip('\']').replace("'", '') + '\n')
        headers += ('検索ワード : ' + searchword + '\n')
        headers += ('created_at : ' + starttime + ' 〜 ' + endtime + '\n')
        headers += ('記事数 : ' + reports.article_count(body) + '\n')
        headers += ('\n')
        headers += ('word\tcount\n')

        #return filename
        return (files.file_format(headers, reports.create_report(body))
)

