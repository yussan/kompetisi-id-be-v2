from flask import Blueprint, request
from flask_restful import Resource, Api
from v2.models.request import getRequest
from v2.helpers.response import api_response
from v2.transformers.request import transform


class RequestApi(Resource):

  # function to get list request
  def get(self):
        Params = {}

        limit = request.args.get('limit')
        status = request.args.get('status')

        # parameter generator
        if(limit):
            Params['limit'] = limit
        if(status):
            Params['status'] = status

        requestdata = []
        result = getRequest(Params)
        for n in result['data']:
            requestdata.append(transform(n))

        return api_response(200, 'ok', {'data': requestdata, 'count': result['count']}), 200

  # function to add list request
  def post(self):
    
    return {}

api_request_bp = Blueprint('api_request', __name__)
api_request = Api(api_request_bp)
api_request.add_resource(RequestApi, '/v2/request')
