from flask import Blueprint, request
import flask_restful

api_competition_bp = Blueprint('api_competition', __name__)
api_competition = flask_restful.Api(api_competition_bp)

class CompetitionApi(flask_restful.Resource):

    def get(self, id):
        print(request.args)
        return {
            'id': id
        }

    def put(self, id):
        pass

    def delete(self, id):
        pass

api_competition.add_resource(CompetitionApi, '/v2/competition/<int:id>')
