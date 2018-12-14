from flask import Blueprint
from flask_restful import Resource, Api
from ..helpers.response import apiResponse
from ..modules.sebangsa import postToSebangsa
from ..config.sebangsa import SBS_API, SBS_COMMUNITY_ID, SBS_COMMUNITY_ROOM, SBS_NEWS_ROOM, SBS_PASSWORD, SBS_USERNAME

class SebangsaAutoPost(Resource):
    def post(self):
        postToSebangsa({
          "room_id": SBS_COMMUNITY_ROOM,
          "group_id": SBS_COMMUNITY_ID,
          "post": "berlomba-lomba dalam kebaikan"
        })
        return apiResponse(200, "posted to Sebangsa")


api_sebangsa_bp = Blueprint("api_sebangsa", __name__)
api_sebangsa = Api(api_sebangsa_bp)

# endpoints
api_sebangsa.add_resource(SebangsaAutoPost, "/v2/sebangsa/autopost")
