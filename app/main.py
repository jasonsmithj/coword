# -*- coding: utf-8 -*-

from app import app
from app.view import routes

app.register_blueprint(routes.application)

