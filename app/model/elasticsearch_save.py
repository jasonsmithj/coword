# -*- coding: utf-8 -*-

from app import app
from elasticsearch import Elasticsearch, helpers

import sys

class ElasticsearchSave():


    def save(self, actions):
        try:
            es = Elasticsearch(app.config['ELASTICSEARCH_ENDPOINT'], port=app.config['ELASTICSEARCH_PORT'], timeout = 180)
            helpers.bulk(es, actions, request_timeout = 180)
        except Exception as e:
            app.logger.info(actions)
            app.logger.error(e.args)
            raise

    def put_setting(self, index):
        settings = {
            "settings":{
                "index.mapping.total_fields.limit": 1000000
            }
        }

        es = Elasticsearch(app.config['ELASTICSEARCH_ENDPOINT'], port=app.config['ELASTICSEARCH_PORT'], timeout = 180)
        try:
            es.indices.put_settings(index=index, body=settings)
        except:
            es.indices.create(index=index)
            es.indices.put_settings(index=index, body=settings)
