# -*- coding: utf-8 -*-

from app import app

if __name__ == '__main__':
    #app.run(debug=app.config['DEBUG'])
    app.run(host='0.0.0.0', port=3000, debug=app.config['DEBUG'])

