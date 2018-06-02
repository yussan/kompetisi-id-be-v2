from flask import Blueprint, request
from flask_restful import Api, Resource
from v2.models.news import getList
from v2.helpers.response import apiResponse
from v2.helpers.encId import decId
from v2.transformers.news import transform


class NewsList(Resource):
    def get(self):
        # get query
        limit = request.args.get('limit')
        lastid = request.args.get('lastid')
        notid = request.args.get('notid')
        status = request.args.get('status')
        tag = request.args.get('tag')

        if (not limit):
            limit = 9

        params = {
            'limit': limit
        }

        # custom params
        if (lastid):
            params['lastid'] = decId(lastid)
        if (tag):
            params['tag'] = tag
        if (status):
            # ref: https://docs.python.org/2/library/stdtypes.html#str.split
            params['status'] = status.split(',')
        else:
            params['status'] = []

        # get news list if id not
        if notid:
            params['notid'] = decId(notid)

        # get data from db
        news = getList(params)

        # return response as standard json
        if(len(news['data']) > 0):
            newsdata = []
            for n in news['data']:
                newsdata.append(transform(n))
            response = {}
            response['data'] = newsdata
            response['count'] = news['count'] 
            
            return apiResponse(200, 'success', response), 200
        else:
            return apiResponse(204), 200

api_newslist_bp = Blueprint('api_newslist', __name__)
api_newslist = Api(api_newslist_bp)
api_newslist.add_resource(NewsList, '/v2/news')
