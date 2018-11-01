from flask import Blueprint, Response
from flask_restful import Resource


class emailVerification(Resource):
    def get(self):
      return {}

api_email_verification_bp = Blueprint('api_email_verification', __name__)

api_email_verification = Api(api_email_verification_bp)

api_email_verification.add_resource(
    emailVerification, '/v2/email-verification')
