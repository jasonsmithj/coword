# -*- coding: utf-8 -*-

from app import app
from elasticsearch import Elasticsearch, helpers

import sys

class ElasticSearch():

    def __init__(self):
        self.es = Elasticsearch(app.config['ELASTICSEARCH_ENDPOINT'], port=app.config['ELASTICSEARCH_PORT'], timeout = 180)

    def save(self, actions):
        try:
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

        mapping = {
          "common": {
            "properties": {
              "created_at": {
                "format" : "YYYY-MM-dd HH:mm:ss","type" : "date"
              }
            }
          }
        }

        try:
            self.es.indices.put_settings(index=index, body=settings)
            self.es.indices.put_mapping(index=index, doc_type='common', body=mapping)
        except:
            self.es.indices.create(index=index)
            self.es.indices.put_settings(index=index, body=settings)
            self.es.indices.put_mapping(index=index, doc_type='common', body=mapping)

    def search(self, keyword, engines, starttime, endtime):

        engn = []
        for engine in engines:
            engn.append(str(engine).lstrip('[\'').rstrip('\']'))


        if len(engn) == 1:
            query = {
            "query": {
              "bool" : {
                "must" : [
                  {"match":{"engine": engn[0]}},
                  {"match" : {"key_word" : keyword}},
                  {"range" : {"created_at" : {"from": starttime, "to": endtime}}}
                ]
              }
            },
              "_source" : {
                "excludes": ["key_word", "url", "engine", "created_at"]
              },
              "size": 200,
              "from":1
            }
        else:
            query = {
            "query": {
              "bool": {
                "should":[
                {
                  "bool": {
                    "must" : [
                      {"match":{"engine": engn[0]}},
                      {"match" : {"key_word" : keyword}},
                      {"range" : {"created_at" : {"from": starttime, "to": endtime}}}
                      ]
                  }
                },
                {
                  "bool": {
                    "must" : [
                      {"match":{"engine": engn[1]}},
                      {"match" : {"key_word" : keyword}},
                      {"range" : {"created_at" : {"from": starttime, "to": endtime}}}
                    ]
                  }
                }
                ]
              }
            },
            "_source" : {
              "excludes": ["key_word", "url", "engine", "created_at"]
            },
            "size": 200,
            "from":1
            }

        try:
            res = self.es.search(index="count_search_result", body=query)
        except Exception as e:
            app.logger.error(e.args)
            raise

        return (res)

