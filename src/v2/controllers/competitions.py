from flask import Blueprint, request
from flask_restful import Api, Resource
from ..models.competitions import getList, getRelated
from ..models.users import getDataByUserKey
from ..helpers.response import apiResponse
from ..helpers.encId import decId
from ..transformers.competition import transform


class CompetitionListApi(Resource):
    def post(self):
        return {
            'status': 201,
            'message': 'kompetisi berhasil dipasang'
        }, 201

    # endpoint to get list competition/browse competition
    def get(self):

        # get query
        limit = request.args.get('limit')
        # lastid in encid format
        lastid = request.args.get('lastid')
        tag = request.args.get('tag')
        search = request.args.get('search')
        mainkat = request.args.get('mainkat')
        subkat = request.args.get('subkat')
        orderby = request.args.get('orderby')
        status = request.args.get('status')
        is_mediapartner = request.args.get('is_mediapartner')
        is_guaranted = request.args.get('is_guaranted')
        is_popular = request.args.get('is_popular')
        by_me = request.args.get("by_me")

        if(not limit):
            limit = 9

        params = {
            'limit': limit
        }

        # custom params
        if (lastid):
            params['lastid'] = decId(lastid)
            params['lastprize'] = lastid
        if (tag):
            params['tag'] = tag
        if (search):
            params['search'] = search
        if (mainkat):
            params['mainkat'] = mainkat
        if (subkat):
            params['subkat'] = subkat
        if (orderby):
            params['orderby'] = orderby
        if (status):
            params['status'] = status

        # get competitio by me (must logged in)
        if by_me:
            userkey = request.headers.get('User-Key')
            if userkey is None:
                # response failed
                return apiResponse(403, "kamu belum login"), 403
            else:
                # get userdata by userkey
                # check userkey on database
                userdata = getDataByUserKey(userkey)
                
                if userdata is None:
                    return apiResponse(403, "kamu belum login"), 403
                else:
                    # added params
                    params['user_id'] = userdata["id_user"]

        params['is_mediapartner'] = is_mediapartner == 'true'
        params['is_guaranted'] = is_guaranted == 'true'
        params['is_popular'] = is_popular == 'true'

        competitions = getList(params)
        response = {}
        response['count'] = competitions['count'] if competitions['count'] else 0
        

        if(len(competitions['data']) > 0):
            comdata = []
            for n in competitions['data']:
                comdata.append(dict(transform(n)))
            response['data'] = comdata
            return apiResponse(200, 'success', response), 200
        else:
            return apiResponse(204, 'Kompetisi tidak ditemukan', response), 200


class CompetitionRelatedApi(Resource):
    def get(self, encid):
        id = decId(encid)

        # get data from db
        competitions = getRelated(id)

        if(len(competitions['data']) > 0):
            comdata = []
            for n in competitions['data']:
                comdata.append(dict(transform(n)))
            response = {}
            response['data'] = comdata

            return apiResponse(200, 'success', response), 200
        else:
            return apiResponse(204, 'Kompetisi tidak ditemukan'), 200


api_competitions_bp = Blueprint('api_competitions', __name__)
api_competitions = Api(api_competitions_bp)
api_competitions.add_resource(CompetitionListApi, '/v2/competitions')
api_competitions.add_resource(
    CompetitionRelatedApi, '/v2/competitions/related/<encid>')
