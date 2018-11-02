from flask import Blueprint, Response
from flask_restful import Resource, Api
from ..modules.crypto import validationEmailVerifToken
from ..helpers.response import apiResponse
from ..models.users import setValidEmail

class emailVerificationRequest(Resource):
    def get(self):
        return {}

class emailVerification(Resource):
    def get(self, token):
        tokenValidate = validationEmailVerifToken(token)
        if type(tokenValidate) is int :
            userId = tokenValidate
            # update user data, and set is_verified to 1
            setValidEmail(userId)

            return apiResponse(200,  'Email kamu telah berhasil terverifikasi')
        else:
            return apiResponse(400,  tokenValidate)


api_email_verification_bp = Blueprint('api_email_verification', __name__)

api_email_verification = Api(api_email_verification_bp)

api_email_verification.add_resource(
    emailVerificationRequest, '/v2/email-verification/request')
api_email_verification.add_resource(
    emailVerification, '/v2/email-verification/<token>')
