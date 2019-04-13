from flask import Blueprint, request
from flask_restful import Api, Resource
from ..models.counter import homeCounter, superSidebarCounter
from ..helpers.response import apiResponse

# endpoint to get count for homepage
class HomeCounter(Resource):
    def get(self):
        count = homeCounter()
        return apiResponse(200, "success", count), 200

# endpoint to get count for super sidebar
class SuperSidebarCounter(Resource):
  def get(self):
      count = superSidebarCounter()
      return apiResponse(200, "success", count), 200


api_counter_bp = Blueprint("api_counter", __name__)
api_counter = Api(api_counter_bp)
api_counter.add_resource(HomeCounter, "/v2/counter/home-counter")
api_counter.add_resource(SuperSidebarCounter, "/v2/counter/super-sidebar")
