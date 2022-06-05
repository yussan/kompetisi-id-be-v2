import os
from flask import Flask, jsonify
from flask_mail import Mail
from v2.helpers.response import apiResponse

# controllers
from v2.controllers.competitions import api_competitions_bp
from v2.controllers.competition import api_competition_detail_bp
from v2.controllers.news_list import api_newslist_bp
from v2.controllers.news import api_news_bp
from v2.controllers.categories import api_categories_bp
from v2.controllers.request import api_request_bp, api_request_super_bp
from v2.controllers.test import api_test_bp
from v2.controllers.auth import api_auth_bp
from v2.controllers.user import api_user_bp
from v2.controllers.feed import api_feed_competition_bp, api_feed_news_bp
from v2.controllers.sitemap import api_sitemap_competition_bp, api_sitemap_news_bp
from v2.controllers.email_verification import api_email_verification_bp
from v2.controllers.sebangsa import api_sebangsa_bp
from v2.controllers.counter import api_counter_bp
from v2.controllers.settings import api_settings_bp
from v2.controllers.forgot_password import api_forgot_password_bp
from v2.controllers.competition_subscription import api_competition_subscription_bp

mail = Mail()

# app init


def create_app(environment=None):
    # ref set template folder https://stackoverflow.com/a/41576661/2780875
    app = Flask(__name__, template_folder='v2/templates')

    # app configuration
    app.config['HOST'] = '0.0.0.0'
    app.config['PORT'] = 18081
    app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'development')
    app.config['FLASK_DEBUG'] = os.environ.get('FLASK_DEBUG', 'true')

    # flask mail config
    app.config['MAIL_SERVER'] = os.environ.get(
        'MAIL_SERVER', 'smtp.sendgrid.net')
    app.config['MAIL_PORT'] = os.environ.get(
        'MAIL_PORT', 25)
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get(
        'MAIL_DEFAULT_SENDER', 'noreply@kompetisi.id')

    mail.init_app(app)
    # end of environment conf

    # handle 404
    @app.errorhandler(404)
    def handleNotFound(e):
        return jsonify(apiResponse(404, 'endpoint tidak ditemukan'))

    # before request
    # app.before_request_funcs = {
    #     "api_competition_detail": []
    # }
    # end of before request

    # blueprint registration
    app.register_blueprint(
        api_competition_detail_bp
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

    app.register_blueprint(
        api_request_super_bp
    )

    app.register_blueprint(
        api_auth_bp
    )

    app.register_blueprint(
        api_test_bp
    )

    app.register_blueprint(
        api_feed_competition_bp
    )

    app.register_blueprint(
        api_feed_news_bp
    )

    app.register_blueprint(
        api_sitemap_competition_bp
    )

    app.register_blueprint(
        api_sitemap_news_bp
    )

    app.register_blueprint(
        api_email_verification_bp
    )

    app.register_blueprint(
        api_user_bp
    )

    app.register_blueprint(
        api_sebangsa_bp
    )

    app.register_blueprint(
        api_counter_bp
    )

    app.register_blueprint(
        api_settings_bp
    )

    app.register_blueprint(
        api_forgot_password_bp
    )

    app.register_blueprint(
        api_competition_subscription_bp
    )
    # end of blueprint registration

    return app
