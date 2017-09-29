# -*- coding: utf-8 -*-

from logging import FileHandler, Formatter
from flask import Flask
from flask_cors import CORS

import sys
import os
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

app = Flask(__name__)

# Load Configration
app.config.from_object('config.CommonConfig')

# Log Settings
if app.config['FLASK_ENV'] != 'development':
    logging.basicConfig(
        filename=app.config['LOG_PATH'],
        level=app.config['LOG_LEVEL'],
        format=app.config['LOG_FORMAT']
    )

fileHandler = FileHandler(app.config['LOG_PATH'], encoding='utf-8')
fileHandler.setFormatter(Formatter(app.config['LOG_FORMAT']))
fileHandler.setLevel(app.config['LOG_LEVEL'])
app.logger.addHandler(fileHandler)

#
CORS(app)

from app import main
