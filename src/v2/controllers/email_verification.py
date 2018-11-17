from flask import Blueprint, Response, request
from flask_restful import Resource, Api
from ..helpers.response import apiResponse
from ..models.users import setValidEmail, getDataById, EmailVerificationBody
from ..transformers.user import transform as transformUser
from ..modules.crypto import validationEmailVerifToken, generateEmailVerifToken
from ..modules.mail import sendEmail

class emailVerificationRequest(Resource):
    def post(self):
        # get user id
        userId = request.form.get('user_id')

        if userId is None :
            return apiResponse(400, "user id tidak ditemukan")
        else :
            # get userdata
            userdata = getDataById(userId)
            if userdata is not None and "id_user" in userdata:
                userdata = transformUser(userdata)

                # send new verification link to user email
                emailVerifToken = generateEmailVerifToken(userdata["id"])
                emailVerifUrl = "https://kompetisi.id/email-verification/" + emailVerifToken
                emailBody = EmailVerificationBody.format(emailVerifUrl, emailVerifUrl)
                sendEmail("Konfirmasi email anda untuk Kompetisi Id", emailBody, [userdata["email"]])
                
                return apiResponse(200, "Link verifikasi telah terkirim, silahkan cek email anda")
            else:  
                return apiResponse(400, "user tidak ditemukan")
            

class emailVerification(Resource):
    def post(self, token):
        tokenValidate = validationEmailVerifToken(token)
        if type(tokenValidate) is int :
            userId = tokenValidate
            # update user data, and set is_verified to 1
            setValidEmail(userId)

            userdata = getDataById(userId)

            if userdata is not None and "id_user" in userdata:
                userdata = transformUser(userdata)
                return apiResponse(201,  'Email kamu telah berhasil terverifikasi', {"data": userdata} ), 201
            else:
                return apiResponse(400, "user tidak ditemukan")
        else:
            return apiResponse(400,  tokenValidate)


api_email_verification_bp = Blueprint('api_email_verification', __name__)

api_email_verification = Api(api_email_verification_bp)

api_email_verification.add_resource(
    emailVerificationRequest, '/v2/email-verification/request')
api_email_verification.add_resource(
    emailVerification, '/v2/email-verification/<token>')
