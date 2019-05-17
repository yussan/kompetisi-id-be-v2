from flask import Blueprint, request
from flask_restful import Resource, Api
from wtforms import Form, StringField, TextAreaField, validators
from ..models.users import getDataByUserKey
from ..helpers.response import apiResponse
from ..transformers.user import transform as transformUser


class SettingProfileValidator(Form):
    username = StringField(
        "Username", [validators.required(), validators.length(min=4, max=50)])
    email = TextAreaField(
        "Email", [validators.required(), validators.length(min=4, max=50)])


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
                # form validation
                form = SettingProfileValidator(request.form)
                if form.validate():
                    userdata = transformUser(userdata)
                    return apiResponse(200, "sukses ubah profil", userdata), 200
                else:
                    # form is not valid
                    # convert error message to string
                    error_messages = ""
                    for key, val in form.errors.items():
                        error_messages += key + ": " + val[0] + " "

                    # get validation error message
                    return apiResponse(400, error_messages), 400

api_settings_bp = Blueprint("api_settings", __name__)
api_settings = Api(api_settings_bp)
api_settings.add_resource(SettingProfile, "/v2/settings/profile")
