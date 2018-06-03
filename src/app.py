import os
from flask import Flask, jsonify
from flask_mail import Mail
from v2.helpers.response import apiResponse
from v2.controllers.competitions import api_competitions_bp
from v2.controllers.competition import api_competition_bp
from v2.controllers.news_list import api_newslist_bp
from v2.controllers.news import api_news_bp
from v2.controllers.categories import api_categories_bp
from v2.controllers.request import api_request_bp

mail = Mail()

# app init
def create_app(environment=None):
    app = Flask(__name__)
    # environment conf
    if not environment:
        environment = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object('config.{}'.format(environment.capitalize()))
    app.config.from_pyfile(
        'config_{}.py'.format(environment.lower()),
        silent=True
    )
    mail.init_app(app)
    # end of environment conf

    # handle 404
    @app.errorhandler(404)
    def handleNotFound(e):
        return jsonify(apiResponse(404, 'endpoint tidak ditemukan'))

    # blueprint registration
    # api v2
    app.register_blueprint(
        api_competition_bp
    )

    app.register_blueprint(
        api_competitions_bp
    )

    app.register_blueprint(
        api_newslist_bp
    )

    app.register_blueprint(
        api_news_bp
    )

    app.register_blueprint(
        api_categories_bp
    )

    app.register_blueprint(
        api_request_bp
    )
    # end of api v2
    # end of blueprint registration


    return app
