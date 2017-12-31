from flask import Blueprint
from flask_restful import Api, Resource, reqparse

class NewsList(Resource):
    def get(self):
        return {}, 200

api_newslist_bp = Blueprint('api_newslist', __name__)
api_newslist = Api(api_newslist_bp)
api_newslist.add_resource(NewsList, '/v2/news')