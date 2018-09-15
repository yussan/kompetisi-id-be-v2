from flask import Blueprint
from flask_restful import Resource, Api
from v2.models.news import getDetail, getList
from v2.helpers.encId import decId
from v2.helpers.response import apiResponse
from v2.transformers.news import transform

class News(Resource):
    def get(self, id):
        # decrypt id
        id = decId(id)
        data = getDetail(id)

        if(data):
            # get related post
            ParamsRelated = {'status': ['published'], 'notid': id, 'limit': 3}
            related = getList(ParamsRelated)

            relateddata = []
            for n in related['data']:
                relateddata.append(transform(n))

            return apiResponse(200, 'success', {'data': dict(transform(data)), 'related': relateddata}), 200
        else:
            return apiResponse(204, 'berita tidak ditemukan'), 204

    def post(self, id):
        return {}, 201

    def delete(self, id):
        return {}, 201


api_news_bp = Blueprint('api_news', __name__)
api_news = Api(api_news_bp)
api_news.add_resource(News, '/v2/news/<string:id>')
