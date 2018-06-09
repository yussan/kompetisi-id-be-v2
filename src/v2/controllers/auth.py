import hashlib
from flask import Blueprint, request
from flask_restful import Api, Resource
from v2.helpers.response import apiResponse
from v2.models.users import login
from v2.transformers.user import transform

class Login(Resource):
  def post(self):
    # ref md5 hash: https://stackoverflow.com/a/5297495/2780875
    params = {
      'username': request.form.get('username'),
      'password': hashlib.md5(request.form.get('password')).hexdigest()
    }

    result = login(params)
    if result is not None:
      return apiResponse(200,  'Login berhasil', {'data': transform(result)})
    else:
      return apiResponse(204)

class Register(Resource):
  def post(self):
    return {}

api_auth_bp = Blueprint('api_auth', __name__)
api_auth = Api(api_auth_bp)
api_auth.add_resource(Login, '/v2/login')
api_auth.add_resource(Register, '/v2/register')