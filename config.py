# -*- coding: utf-8 -*-

import os
import sys
import re
import logging
from dotenv import load_dotenv


class CommonConfig(object):
    FLASK_ENV = os.environ.get('FLASK_ENV')

    if FLASK_ENV == 'development':
        LOG_LEVEL = logging.INFO
        DEBUG = True
        ELASTICSEARCH_ENDPOINT = '172.122.6.170'
        ELASTICSEARCH_PORT = 9200
    else:
        LOG_LEVEL = logging.WARNING
        DEBUG = False
        ELASTICSEARCH_ENDPOINT = '127.0.0.1'
        ELASTICSEARCH_PORT = 9200

    JSON_AS_ASCII = False
    LOG_PATH = 'logs/app.log'
    LOG_FORMAT = 'time:%(asctime)s\tlevel:%(levelname)s\tfile:%(filename)s\tmodule:%(module)s\tmethod:%(funcName)s\tline:%(lineno)d\tmessage:%(message)s'

    NEOLOGD_PATH = '/usr/local/lib/mecab/dic/mecab-ipadic-neologd'

    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    GOOGLE_CX = os.environ.get("GOOGLE_CX")

    TMP_PATH = os.path.join(os.path.dirname(__file__), 'tmp/')
    DOWNLOAD_PATH = os.path.join(os.path.dirname(__file__), 'download/')

