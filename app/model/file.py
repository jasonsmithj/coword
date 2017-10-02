# -*- coding: utf-8 -*-

from app import app

class File():
    def save(self, body, filename):
        try:
            with open(filename , 'w' ) as f:
                f.write(body)
        except Exception as e:
            app.logger.error(e)
            raise


