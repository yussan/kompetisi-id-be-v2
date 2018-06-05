from flask import Blueprint, request
from flask_restful import Resource, Api
from flask_mail import Message
from v2.modules.mail import sendEmail

class TestEmail(Resource):
    def post(self):
        emailBody = '<h1>This is HTML body</h1>'
        sendEmail('Another Test from kompetisi.id', emailBody, ['yussan@mailinator.com'])

        return {
            'status': 200,
            'message': 'success send email'
        }


api_test_bp = Blueprint('api_test', __name__)
api_test = Api(api_test_bp)
api_test.add_resource(TestEmail, '/v2/test/email')
