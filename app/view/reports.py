# -*- coding: utf-8 -*-

from app import app
from app.model.search import Search
from app.model.elasticsearch import ElasticSearch
from app.model.reports import Reports
from app.model.file import File


class Reports():

    def create(self):
        
        headers = """
        検索エンジン	$engine
        検索ワード	$keyword
        created_at	$starttime 〜 $endtime
        """

        return filename

