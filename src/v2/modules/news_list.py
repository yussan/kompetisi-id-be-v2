from flask import Blueprint, request
from flask_restful import Api, Resource
from v2.models.news import getList
from libraries.response import api_response

class NewsList(Resource):
    def get(self):
        # get url query
        limit = request.args.get('limit')
        lastid = request.args.get('lastid')

        if (not limit): limit = 10

        # get data from db
        data = getList({
            'limit': limit,
            'lastid': lastid
        })

        # return response as standard json
        if(len(data) > 0):
            return api_response(200, 'success', {'results': data}), 200
        else:
            return api_response(204), 204

api_newslist_bp = Blueprint('api_newslist', __name__)
api_newslist = Api(api_newslist_bp)
api_newslist.add_resource(NewsList, '/v2/news')

