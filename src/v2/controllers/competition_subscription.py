# pip modules
from flask import Blueprint, request
from flask_restful import Api, Resource 

# transformers
from ..transformers.competition import transform as transformCompetition

# models
from ..models.competitions_subscription import subscribeAction, subscribeList
from ..models.users import getDataByUserKey

# helpers
from ..helpers.response import apiResponse
from ..helpers.encId import decId

class CompetitionSubscribe(Resource):
  def get(self):
    userkey = request.headers.get('User-Key')

    if userkey == None:
        return apiResponse(403, 'anda tidak memiliki akses disini'), 403
    else:
      # check userkey on database
      userdata = getDataByUserKey(userkey)

      if userdata is None:
          return apiResponse(403, 'akun tidak ditemukan'), 403

      Params = {
        'user_id': userdata['id_user']
      } 

      # custom params for http query
      lastid = request.args.get('lastid')
      limit = request.args.get('limit')

      if lastid != None : Params['lastid'] = decId(lastid)
      if limit != None : Params['limit'] = limit

      # get data subscribed competitions from database
      competitions = subscribeList(Params)

      response = {}
      response['count'] = competitions['count'] if competitions['count'] else 0


      if len(competitions['data']) > 0:
          comdata = []
          for n in competitions['data']:
              comdata.append(dict(transformCompetition(n)))
          response['data'] = comdata
          return apiResponse(200, 'success', response), 200
      else:
          return apiResponse(204, 'Kompetisi tidak ditemukan', response), 200

  def post(self):

    userkey = request.headers.get('User-Key')

    if userkey == None:
        return apiResponse(403, 'anda tidak memiliki akses disini'), 403
    else:
        # check userkey on database
        userdata = getDataByUserKey(userkey)

        if userdata is None:
            return apiResponse(403, 'akun tidak ditemukan'), 403

        Params = {
          'competition_id': decId(request.form.get('competition_id')),
          'user_id': userdata['id_user']
        }
        
        subscribeAction(Params)

        # response as action success
        return apiResponse(201, 'Aksi berhasil'), 201

api_competition_subscription_bp = Blueprint('api_competition_subscription', __name__)

api_competition_subscription = Api(api_competition_subscription_bp)

api_competition_subscription.add_resource(CompetitionSubscribe, '/v2/competition-subscription')