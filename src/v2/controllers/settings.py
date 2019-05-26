from flask import Blueprint, request
from flask_restful import Resource, Api
from wtforms import Form, StringField, TextAreaField, validators
from ..models.users import getDataByUserKey, updateData
from ..helpers.response import apiResponse
from ..transformers.user import transform as transformUser, transformAvatar
from ..modules.file_upload import handleUpload
import os
import json


class SettingProfile(Resource):
    def put(self):

        # get userkey
        userkey = request.headers.get('User-Key')

        if userkey is None:
            # user not login
            return apiResponse(403, "Kamu tidak memiliki akses disini")
        else:
            # get user profile by userkey
            userdata = getDataByUserKey(userkey)
            if userdata is None:
                # userdata not found
                return apiResponse(403, "Kamu tidak memiliki akses disini")
            else:

                userdata = transformUser(userdata)

                # generate params to update database
                params = {
                    "fullname": request.form.get("fullname"),
                    "alamat": request.form.get("address")
                }
                # check is upload new avatar
                if len(request.files) > 0 and request.files["avatar"] != None :
                    # process upload avatar
                    upload_dir_db = "/" + userdata["username"] + "/avatar"
                    upload_dir = os.environ.get(
                        "MEDIA_DIR", "../media-kompetisiid") + upload_dir_db
                    input_avatar = request.files["avatar"]
                    # start upload avatar
                    uploadAvatar = handleUpload(upload_dir, input_avatar, upload_dir_db)
                    
                    # set params["avatar"] value
                    params["avatar"] = json.dumps({
                        "small": "/" + userdata["username"] + "/avatar/" + uploadAvatar["filename"] ,
                        "original": "/" + userdata["username"] + "/avatar/" + uploadAvatar["filename"]
                    })
                    userdata["avatar"] = transformAvatar(params["avatar"])

                # update database
                updateData(params, userdata["id"])

                userdata["fullname"] = params["fullname"] 
                userdata["address"] = params["alamat"]

                return apiResponse(200, "sukses ubah profil", userdata), 200

api_settings_bp = Blueprint("api_settings", __name__)
api_settings = Api(api_settings_bp)
api_settings.add_resource(SettingProfile, "/v2/settings/profile")
