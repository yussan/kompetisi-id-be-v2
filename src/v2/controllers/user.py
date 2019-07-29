from flask import Blueprint, request
from flask_restful import Api, Resource
from ..models.users import getDataByUsername, getUsers
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

class UserList(Resource):
  def get(self):
    params = {
      "banned": request.args.get('banned') == "true",
      "verified": request.args.get('verified') == "true",
      "unverified": request.args.get('unverified') == "true",
    }

    lastid = request.args.get('lastid')
    if(lastid != None): params["lastid"] = lastid

    result = getUsers(params)
    if result != None and len(result) > 0:
        nextdata = []
        for n in result:
          # if "user_key" in n :
          n = transform(n)
          del n["user_key"]
          nextdata.append(n)
        # result = transform(result)
        # # delete userkey
        return apiResponse(200,  'success', {'data': nextdata})
    else:
        return apiResponse(204)

api_user_bp = Blueprint('api_user', __name__)
api_user = Api(api_user_bp)

api_user.add_resource(Profile, '/v2/user/<username>')
api_user.add_resource(UserList, '/v2/users')

