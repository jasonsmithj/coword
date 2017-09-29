# -*- coding: utf-8 -*-

import urllib
from urllib3.exceptions import HTTPError
from readability.readability import Document
from bs4 import BeautifulSoup
import json
import html2text
import ssl
import re

from app import app

class Search():

    def scraping(self, url):
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            req = urllib.request.Request(url, None, app.config['HEADERS'])
            url = urllib.request.urlopen(req)
            s = url.read()
            article = Document(s).summary()
            return html2text.html2text(article)
        except Exception as e:
            app.logger.error(e.args)
            return url

    def google_search(self, words):

        NUM = 10
        val = []

        url = 'https://www.googleapis.com/customsearch/v1?'
        params = {
            'key': app.config['GOOGLE_API_KEY'],
            'q': words,
            'cx':app.config['GOOGLE_CX'],
            'alt':'json',
            'lr' :'lang_ja',
        }

        start = 1

        try:
            for i in range(0,NUM):
                params['start'] = start
                req_url = url + urllib.parse.urlencode(params)
                res = urllib.request.urlopen(req_url)
                dump = json.loads(res.read())

                for y in range (0,NUM):
                    val.append(dump['items'][y]['link'])
                    if not 'nextPage' in dump['queries']:
                        break
                    start = int(dump['queries']['nextPage'][0]['startIndex'])
        except Exception as e:
            app.logger.error(e.args)
            return ('NG')

        return val

    def google_news_search(self, words):

        val = []
        url = 'http://news.google.com/news?'
        params = {
            'hl': 'ja',
            'ned': 'us',
            'ie': 'UTF-8',
            'oe': 'UTF-8',
            'output': 'rss',
            'num': 100,
            'q': words
        }

        req_url = url + urllib.parse.urlencode(params)
        html = urllib.request.urlopen(req_url)
        soups = BeautifulSoup(html, "html.parser").find_all("guid")
        val = []
        for soup in soups:
            soup = ((str(soup)).lstrip('<guid ispermalink="false">tag:news.google.com,2005:cluster='))
            soup = (soup.rstrip('</guid>'))
            val.append(soup)

        return val
