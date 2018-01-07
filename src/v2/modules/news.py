from flask import Blueprint
from flask_restful import Resource, Api

class News(Resource):
    def get(self, id):
        return {}, 200

    def post(self, id):
        return {}, 201

    def delete(self, id):
        return {}, 201

api_news_bp = Blueprint('api_news', __name__)
api_news = Api(api_news_bp)
api_news.add_resource(News, '/v2/news/<int:id>')