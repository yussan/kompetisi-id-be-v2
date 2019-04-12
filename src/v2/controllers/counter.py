from flask import Blueprint, request
from flask_restful import Api, Resource
from ..models.counter import homeCounter
from ..helpers.response import apiResponse

class HomeCounter(Resource):
    def get(self):
        stats = homeCounter()
        return apiResponse(200, "success", stats), 200


api_counter_bp = Blueprint("api_counter", __name__)
api_counter = Api(api_counter_bp)
api_counter.add_resource(HomeCounter, "/v2/home-counter")
