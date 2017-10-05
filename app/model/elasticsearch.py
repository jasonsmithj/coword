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

    def mapping(self, index):
        mapping = {
          "common": {
            "properties": {
              "engine":     { "type": "text", "index" : "not_analyzed" },
              "key_word":   { "type": "text", "index" : "not_analyzed" },
              "url":        { "type": "text", "index" : "not_analyzed" },
              "created_at": { "format" : "YYYY-MM-dd HH:mm:ss","type" : "date" }
            }
          }
        }
        return self.es.indices.put_mapping(index=index, doc_type='common', body=mapping)

    def put_setting(self, index):
        elasti_cserch = ElasticSearch()
        settings = {
            "settings":{
                "index.mapping.total_fields.limit": 1000000
            }
        }

        try:
            self.es.indices.put_settings(index=index, body=settings)
        except:
            self.es.indices.create(index=index)
            self.es.indices.put_settings(index=index, body=settings)
            elasti_cserch.mapping(index)

    def search(self, keyword, engines, starttime, endtime, index):
        elasti_cserch = ElasticSearch()

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
            }
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
            }
            }

        try:
            elasti_cserch.mapping('count_' + index + '_result')
            res = self.es.search(index=('count_' + index + '_result'), body=query)
        except Exception as e:
            app.logger.error(e.args)
            raise

        return (res)

