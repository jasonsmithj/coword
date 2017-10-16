# -*- coding: utf-8 -*-

from app import app
from app.model.search import Search
from app.model.elasticsearch import ElasticSearch
from app.model.report import Report
from app.model.file import File

import re
import textwrap

class Reports():

    def create(self, searchword, engine, starttime, endtime, index, ngword = '空前絶後のぉ！'):
        es = ElasticSearch()
        reports = Report()
        files = File()

        body = es.search(searchword, engine, starttime, endtime, index)

        search_engine = str(','.join(engine)).lstrip('[\'').rstrip('\']').replace("'", '')
        headers = textwrap.dedent(f'''
        Search Engine\t:\t{search_engine}
        Search Word\t:\t{searchword}
        Time Range\t:\t{starttime} ~ {endtime}
        Article Count\t:\t{reports.article_count(body)}

        Word\tCount
        ''').strip()

        return (files.file_format(headers, reports.create_report(body), ngword)
)

