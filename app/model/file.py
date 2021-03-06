# -*- coding: utf-8 -*-

from app import app

from datetime import datetime

class File():
    def save(self, body):
        now_date = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = (now_date + '.txt')
        filepath = (app.config['DOWNLOAD_PATH'] + filename)
        try:
            with open(filepath , 'w' ) as f:
                f.write(body)
        except Exception as e:
            app.logger.error(e)
            raise
        return filename

    def file_format(self, headers, bodys, ngword):
        files = File()
        ngwords = ngword.splitlines()
        report_str = headers
        report_str += ('\n')

        for body in bodys:
            if not body[0] in ngwords:
                report_str += (body[0] + '\t' + str(body[1]) + '\n')
        return (files.save(report_str))
