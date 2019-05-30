from flask import Blueprint, request
from flask_restful import Resource, Api
from wtforms import Form, StringField, TextAreaField, validators
from ..models.users import getDataByUserKey, updateData, EmailVerificationBody, checkEmail
from ..helpers.response import apiResponse
from ..transformers.user import transform as transformUser, transformAvatar
from ..modules.file_upload import handleUpload
from wtforms import Form, StringField, validators
from ..modules.mail import sendEmail
import os
import json
import hashlib

class SettingAccountValidator(Form):
    email = StringField("email", [validators.required(), validators.length(min=4, max=50)])
    password = StringField("password", [validators.required(), validators.length(min=4, max=50)])


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

                return apiResponse(200, "sukses ubah profil", {"data": userdata}), 200

class SettingAccount(Resource):
    def put(self):

        # form validation
        form = SettingAccountValidator(request.form)

        if form.validate():
            # get userkey
            userkey = request.headers.get('User-Key')

            if userkey is None:
                # user not login
                return apiResponse(403, "Kamu tidak memiliki akses disini")
            else:
                # get user profile by userkey
                userdatadb = getDataByUserKey(userkey)
                if userdatadb is None:
                    # userdata not found
                    return apiResponse(403, "Kamu tidak memiliki akses disini")
                else:
                    userdata = transformUser(userdatadb)
                    currentPassword = hashlib.md5(request.form.get("password")).hexdigest()
                    
                    # check is send password same as current password
                    if userdatadb["password"] == currentPassword:
                        params = {}
                        
                        # check is update password
                        if request.form.get("new_password") != None :
                            currentPassword = hashlib.md5(request.form.get("new_password")).hexdigest()
                            
                        # check is update email
                        if request.form.get("email") != userdata["email"]:

                            # check is email already used
                            resCheckEmail = checkEmail(request.form.get("email"))

                            if resCheckEmail is not None:
                                return apiResponse(422, "Email sudah digunakan user lain")
                            else:
                                params["email"] = request.form.get("email")
                                params["is_verified"] = 0

                                # send email verification
                                emailVerifUrl = "https://kompetisi.id/email-verification/" + userdata["user_key"]
                                emailBody = EmailVerificationBody.format(emailVerifUrl, emailVerifUrl)
                                sendEmail("Konfirmasi email anda untuk Kompetisi Id",
                                        emailBody, [params["email"]])

                        # update database
                        params["password"] = currentPassword
                        updateData(params, userdata["id"])
                        
                        return apiResponse(200, "Sukses update akun")
                    else: 
                        return apiResponse(422, "Password tidak sesuai")
        else :
            # print form.errors
            # convert error message to string
            error_messages = ""
            for key, val in form.errors.items():
                error_messages += key + ": " + val[0] + " "
                
            # get validation error message
            return apiResponse(400, error_messages), 400

api_settings_bp = Blueprint("api_settings", __name__)
api_settings = Api(api_settings_bp)
api_settings.add_resource(SettingProfile, "/v2/settings/profile")
api_settings.add_resource(SettingAccount, "/v2/settings/account")
