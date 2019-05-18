from flask import Blueprint, request
from flask_restful import Api, Resource
from ..models.users import getDataByUsername
from ..transformers.user import transform
from ..helpers.response import apiResponse
class Profile(Resource):
  def get(self, username):
    result = getDataByUsername(username)
    
    if result != None:
        result = transform(result)
        # delete userkey
        if "user_key" in result :
          del result["user_key"]
        return apiResponse(200,  'success', {'data': result})
    else:
        return apiResponse(204)

api_user_bp = Blueprint('api_user', __name__)
api_user = Api(api_user_bp)

api_user.add_resource(Profile, '/v2/user/<username>')

