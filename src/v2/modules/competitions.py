from flask import Blueprint
from flask_restful import Api, Resource, reqparse
import logging

# dummy data
competitions = [
    {'id': 1, 'title':'competition title 1', 'desc': 'this is short desc'},
    {'id': 2, 'title': 'competition title 2', 'desc': 'this is short desc'},
    {'id': 3, 'title': 'competition title 3', 'desc': 'this is short desc'},
]

class CompetitionListApi(Resource):
    def post(self):
        return {
            'status': 201,
            'message': 'kompetisi berhasil dipasang'
               }, 201
    def get(self):
        return {
            'status': 200,
            'data': competitions
               }, 200

api_competitions_bp = Blueprint('api_competitions', __name__)
api_competitions = Api(api_competitions_bp)
api_competitions.add_resource(CompetitionListApi, '/v2/competitions')