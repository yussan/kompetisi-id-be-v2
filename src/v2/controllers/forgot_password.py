from flask import Blueprint, request
from flask_restful import Api, Resource
from wtforms import Form, StringField, validators
from ..modules.mail import sendEmail
from ..helpers.response import apiResponse
from ..modules.crypto import generateKIToken, validationKIToken, EMAIL_VERIFICATION_KEY
from ..models.users import updateDataByEmail, checkEmail
import hashlib


class ForgotPasswordValidator(Form):
    email = StringField("email", [validators.required()])


class ChangePasswordValidator(Form):
    token = StringField("token", [validators.required()])
    password = StringField("password", [validators.required(), validators.EqualTo(
        'password_conf', message='Password konfirmasi tidak cocok')])
    password_conf = StringField("password", [validators.required()])


class ForgotPassword(Resource):
    # controller to forgot password
    def post(self):
        # formdata validator
        form = ForgotPasswordValidator(request.form)

        if form.validate():
            # get email from formdata
            email = request.form.get("email")

            # check is email available
            resCheckEmail = checkEmail(email)

            if resCheckEmail is not None:
                # generate new forgot password token
                change_password_token = generateKIToken(
                    email, EMAIL_VERIFICATION_KEY)

                # send change password link to email
                change_password_link = "https://kompetisi.id/change-password/" + change_password_token
                email_body = '''
                <p>
                Untuk mengganti password, silahkan kunjungi link berikut ini <a target="_blank" href="{link}">ubah password</a>.
                <br/>
                <br/>
                Atau kamu bisa mengunjungi link berikut ini <span style="color:gray">{link}</span>
                <br/>
                <br/>
                </p>
                '''.format(link=change_password_link)
                sendEmail('Lanjutkan Untuk Ganti Password - Kompetisi Id',
                          email_body, [email])

                return apiResponse(200, "Kami telah mengirim link ganti password ke email kamu"), 200
            else:
                return apiResponse(400, "Email tidak terdaftar di Kompetisi Id"), 400
        else:
            error_messages = ""
            for key, val in form.errors.items():
                error_messages += key + ": " + val[0] + " "

            # get validation error message
            return apiResponse(400, error_messages), 400


class ChangePassword(Resource):
    # controller to change password using token from email
    def post(self):
        # formdata validator
        form = ChangePasswordValidator(request.form)

        if form.validate():
            # token validation
            tokenValidation = validationKIToken(
                request.form.get("token"), EMAIL_VERIFICATION_KEY)
            if tokenValidation["is_valid"]:

                # get new password
                password = request.form.get("password")
                email = tokenValidation["value"]

                # hash password and change password by email
                newpassword = hashlib.md5(password)

                updateDataByEmail({"password": newpassword.hexdigest()}, email)

                return apiResponse(200, "Ubah password untuk email {email} telah berhasil silahkan login lagi".format(email=email)), 200
            else:
                # token not valid
                return apiResponse(400, tokenValidation["message"]), 400

        else:
            error_messages = ""
            for key, val in form.errors.items():
                error_messages += key + ": " + val[0] + " "

            # get validation error message
            return apiResponse(400, error_messages), 400


api_forgot_password_bp = Blueprint("api_forgot_password", __name__)

api_forgot_password = Api(api_forgot_password_bp)

api_forgot_password.add_resource(ForgotPassword, "/v2/forgot-password")
api_forgot_password.add_resource(ChangePassword, "/v2/change-password")
