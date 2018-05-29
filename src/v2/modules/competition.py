from flask import Blueprint, request
from flask_restful import Api, Resource
from v2.helpers.encId import decId
from v2.models.competitions import getDetail
from v2.transformers.competition import transform
from v2.helpers.response import api_response

api_competition_bp = Blueprint('api_competition', __name__)
api_competition = Api(api_competition_bp)


class CompetitionApi(Resource):

    def get(self, encid):
        id = decId(encid)
        competition = getDetail(id)

        if('id_kompetisi' in competition['data']):
            competition['data'] = transform(competition['data'])
            # competition found
            return api_response(200, 'success', competition), 200
        else:
            # component not found
            return api_response(204), 200

    def put(self, encid):
        pass

    def delete(self, encid):
        pass


api_competition.add_resource(CompetitionApi, '/v2/competition/<encid>')
