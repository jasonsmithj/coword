# -*- coding: utf-8 -*-

from app import app
from elasticsearch import Elasticsearch, helpers

import sys

class ElasticsearchSave():

    def __init__(self):
        self.es = Elasticsearch(app.config['ELASTICSEARCH_ENDPOINT'], port=app.config['ELASTICSEARCH_PORT'], timeout = 180)

    def save(self, actions):
        try:
            self.es = Elasticsearch(app.config['ELASTICSEARCH_ENDPOINT'], port=app.config['ELASTICSEARCH_PORT'], timeout = 180)
            helpers.bulk(self.es, actions, request_timeout = 180)
        except Exception as e:
            app.logger.error(e.args)
            raise

    def put_setting(self, index):
        settings = {
            "settings":{
                "index.mapping.total_fields.limit": 1000000
            }
        }

        self.es = Elasticsearch(app.config['ELASTICSEARCH_ENDPOINT'], port=app.config['ELASTICSEARCH_PORT'], timeout = 180)
        try:
            self.es.indices.put_settings(index=index, body=settings)
        except:
            self.es.indices.create(index=index)
            self.es.indices.put_settings(index=index, body=settings)
