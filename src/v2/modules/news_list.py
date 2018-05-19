from flask import Blueprint, request
from flask_restful import Api, Resource
from v2.models.news import getList
from libraries.response import api_response
from v2.transformers.news import transform

class NewsList(Resource):
    def get(self):
        # get url query
        limit = request.args.get('limit')
        lastid = request.args.get('lastid')
        status = request.args.get('status')

        if (not limit): limit = 10
        
        params = {
            'limit': limit
        }

        # custom params
        if (lastid): params['lastid'] = lastid
        if (status): 
            # ref: https://docs.python.org/2/library/stdtypes.html#str.split
            params['status'] = status.split(',')
        else:
            params['status'] = []

        # get data from db
        data = getList(params)

        # return response as standard json
        if(len(data) > 0):
            news = []
            for n in data:
                news.append(dict(transform(n)))

            return api_response(200, 'success', {'data': news}), 200
        else:
            return api_response(204), 204

api_newslist_bp = Blueprint('api_newslist', __name__)
api_newslist = Api(api_newslist_bp)
api_newslist.add_resource(NewsList, '/v2/news')

