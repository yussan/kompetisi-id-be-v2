import os
from flask import Flask, jsonify
from v2.helpers.response import api_response
from v2.modules.competitions import api_competitions_bp
from v2.modules.competition import api_competition_bp
from v2.modules.news_list import api_newslist_bp
from v2.modules.news import api_news_bp

# app init
def create_app(environment=None):
    app = Flask(__name__)

    # environment conf
    if not environment:
        environment = os.environ.get('FLASK_CONFIG', 'development')
    app.config.from_object('config.{}'.format(environment.capitalize()))
    app.config.from_pyfile(
        'config_{}.py'.format(environment.lower()),
        silent=True
    )
    # end of environment conf

    # handle 404
    @app.errorhandler(404)
    def handleNotFound(e):
        return jsonify(api_response(404, 'endpoint tidak ditemukan'))

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
    # end of api v2
    # end of blueprint registration

    return app
