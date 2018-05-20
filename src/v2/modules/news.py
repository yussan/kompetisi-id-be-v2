from flask import Blueprint
from flask_restful import Resource, Api
from v2.models.news import getDetail, getList
from libraries.response import api_response
from v2.transformers.news import transform


class News(Resource):
    def get(self, id):
        data = getDetail(id)

        if(data):
            # get related post
            ParamsRelated = {'status':['published'], 'notid': id, 'limit': 3}
            related_data = getList(ParamsRelated)

            related = []
            for n in related_data:
                related.append(dict(transform(n)))

            return api_response(200, 'success', {'data': dict(transform(data)), 'related': related}), 200
        else:
            return api_response(204, 'berita tidak ditemukan'), 204

    def post(self, id):
        return {}, 201

    def delete(self, id):
        return {}, 201


api_news_bp = Blueprint('api_news', __name__)
api_news = Api(api_news_bp)
api_news.add_resource(News, '/v2/news/<int:id>')
