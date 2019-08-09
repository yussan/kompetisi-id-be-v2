import json
from flask import request, jsonify
from ..helpers.response import apiResponse
from ..models.users import getDataByUserKey

# only moderator and admin can through access


def isModerator():
    userKey = request.headers.get('User-Key')
    if userKey == None:
        return jsonify(apiResponse(401, 'Not authorized')), 401
    else:
        # get userdata by userKey and check level, level must be (admin or moderator)
        userdata = getDataByUserKey(userKey)
        if userdata is None:
            return jsonify(apiResponse(401, "akun tidak ditemukan")), 401
        elif(userdata["level"] != "admin" and userdata["level"] != "moderator"):
            return jsonify(apiResponse(401, 'Not authorized')), 401
