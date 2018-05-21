from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from v2.models.competitions import getList
from libraries.response import api_response
from v2.transformers.competition import transform

class CompetitionListApi(Resource):
    def post(self):
        return {
            'status': 201,
            'message': 'kompetisi berhasil dipasang'
               }, 201

    # endpoint to get list competition/browse competition
    def get(self):

        # get query
        limit = request.args.get('limit')
        lastid = request.args.get('lastid')
        tag = request.args.get('tag')

        if(not limit):
            limit = 9

        params = {
            'limit': limit
        }

        # custom params
        if (lastid):
            params['lastid'] = lastid
        if (tag):
            params['tag'] = tag

        competitions = getList(params)

        if(len(competitions) > 0):
            comdata = []
            for n in competitions['data']:
                comdata.append(dict(transform(n)))
            response = {}
            response['data'] = comdata
            response['count'] = competitions['count'] 

            return api_response(200, 'success', response), 200
        else:
            return api_response(204), 204

        return {
            'status': 200,
            'data': competitions
               }, 200

api_competitions_bp = Blueprint('api_competitions', __name__)
api_competitions = Api(api_competitions_bp)
api_competitions.add_resource(CompetitionListApi, '/v2/competitions')