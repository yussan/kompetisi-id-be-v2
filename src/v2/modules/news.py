from flask import Blueprint
from flask_restful import Resource, Api
from v2.models.news import getDetail
from libraries.response import api_response

class News(Resource):
    def get(self, id):
        data = getDetail(id)
        if (len(data) > 0):
            return api_response(200, 'success', {'results': data}), 200
        else:
            return api_response(204, 'berita tidak ditemukan'), 200

    def post(self, id):
        return {}, 201

    def delete(self, id):
        return {}, 201

api_news_bp = Blueprint('api_news', __name__)
api_news = Api(api_news_bp)
api_news.add_resource(News, '/v2/news/<int:id>')