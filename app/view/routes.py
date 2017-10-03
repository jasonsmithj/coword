# -*- coding: utf-8 -*-

from app import app
from app.view.word_cloud import WordSearch
from app.view.article import Article
from app.view.reports import Reports

from flask import Flask, Blueprint, render_template, jsonify, abort, request, send_from_directory

application = Blueprint('routes', __name__,template_folder='templates')

@application.route("/", methods=['GET'])
def coword_index():
    return render_template('index.html')

@application.route("/word_cloud/", methods=['GET'])
def word_cloud():
    return render_template('word_cloud/index.html')

@application.route("/word_cloud/check", methods=['GET'])
def word_cloud_check():
    return render_template('word_cloud/check.html',
        searchword = request.args.get('searchword'),
        engine = request.args.get('engine')
    )

@application.route("/word_cloud/result", methods=['GET'])
def word_cloud_result():
    word_seach = WordSearch()
    result = word_seach.search(request.args.get('searchword'), request.args.get('engine'))
    return render_template('word_cloud/result.html', result = result)

@application.route("/article", methods=['GET'])
def article():
    return render_template('article/index.html')

@application.route("/article/check", methods=['POST'])
def articl_checke():
    article = Article()
    try:
        the_file = request.files['file_name']
        the_file.save(app.config['TMP_PATH'] + the_file.filename)
        article_url = article.csv_to_url((app.config['TMP_PATH'] + the_file.filename))
    except Exception as e:
        app.logger.info(e)
        return render_template('article/result.html', result='Faild')
    return render_template('article/check.html', filename = the_file.filename, url = article_url)

@application.route("/article/result", methods=['GET'])
def article_result():
    article = Article()
    filename = (app.config['TMP_PATH'] + request.args.get('filename'))
    article_url = article.csv_to_url(filename)
    result = article.create_record(article_url)
    article.delete_file(filename)
    return render_template('word_cloud/result.html', result = result)

@application.route("/reports", methods=['GET'])
def reports():
    return render_template('reports/index.html')

@application.route("/reports/check", methods=['GET'])
def reports_check():
    return render_template('reports/check.html',
        searchword = request.args.get('searchword'),
        starttime = request.args.get('starttime'),
        endtime = request.args.get('endtime'),
        engine = str(request.args.getlist('engine')).lstrip('[\'').rstrip('\']').replace("'", '') 
    )

@application.route("/reports/result", methods=['GET'])
def reports_result():
    reports = Reports()
    result = reports.create(
        request.args.get('searchword'),
        request.args.getlist('engine'),
        request.args.get('starttime'),
        request.args.get('endtime'),
    )
    return render_template('reports/result.html', result = result)

@application.route("/reports/download", methods=['GET'])
def reports_download():
    return send_from_directory(directory=app.config['DOWNLOAD_PATH'], filename=request.args.get('filename'), as_attachment=True)

@application.errorhandler(400)
def bad_request(error):
    app.logger.info('400 '+error.description['message'])

    errors = {
        'status': 400,
        'code': error.description['code'],
        'message': error.description['message']
    }

    if 'errors' in error.description:
        errors['errors'] = []
        for error in error.description['errors']:
            errors['errors'].append({
                'field': error['field'],
                'code': error['code']
            })

    return jsonify(errors), 400


@application.errorhandler(401)
def unauthorized(error):
    app.logger.info('400 '+error.description['message'])
    return jsonify({
        'status': 401,
        'code': 'unauthorized',
        'message': 'You need to sign up to access this resource.'
    }), 401


@application.errorhandler(403)
def forbidden(error):
    app.logger.info('403 You have no permission to access this resource.')
    return jsonify({
        'status': 403,
        'code': 'forbidden',
        'message': 'You have no permission to access this resource.'
    }), 403


@application.errorhandler(404)
def not_found(error):
    app.logger.info('404 The endpoint does not exist.')
    return jsonify({
        'status': 404,
        'code': 'not_found',
        'message': 'The endpoint does not exist.'
    }), 404


@application.errorhandler(405)
def method_not_allowed(error):
    app.logger.info('405 The method is not allowed.')
    return jsonify({
        'status': 405,
        'code': 'method_not_allowed',
        'message': 'The method is not allowed.'
    }), 405


@application.errorhandler(408)
def request_timeout(error):
    app.logger.info('408 Processing could not be returned even after 10 seconds or more.')
    return jsonify({
        'status': 408,
        'code': 'request_timeout',
        'message': 'Processing could not be returned even after 10 seconds or more.'
    }), 408


@application.errorhandler(500)
def internal_server_error(error):
    message = 'Internal Server Error'
    app.logger.info('500 '+message)

    return jsonify({
        'status': 500,
        'code': 'internal_server_error',
        'message': message
    }), 500

