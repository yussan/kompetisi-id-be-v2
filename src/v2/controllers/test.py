from flask import Blueprint, request
from flask_restful import Resource, Api
# from flask_mail import Message
from v2.modules.mail import sendEmail


class TestEmail(Resource):
    def post(self):
        sendEmail('Another Test from kompetisi.id',
                  EmailThanksBody, ['yussan@mailinator.com'])

        return {
            'status': 200,
            'message': 'success send email'
        }


EmailThanksBody = """
<div class="">
        <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 30px; padding-left: 30px; padding-top: 30px; padding-bottom: 15px;"><![endif]-->
        <div style="color:#555555;font-family:'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;line-height:120%; padding-right: 30px; padding-left: 30px; padding-top: 30px; padding-bottom: 15px;">
            <div style="font-family:Montserrat, 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;font-size:12px;line-height:14px;color:#555555;text-align:left;">
            <p style="margin: 0;font-size: 12px;line-height: 14px;text-align: center">
                <span style="font-size: 18px; line-height: 21px;">
                <strong>Terimakasih Telah Melakukan Permintaan Pasang Kompetisi</strong>
                </span>
            </p>
            </div>
        </div>
        <!--[if mso]></td></tr></table><![endif]-->
        </div>

        <div class="">
        <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top: 0px; padding-bottom: 5px;"><![endif]-->
        <div style="color:#E15A5A;font-family:'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;line-height:120%; padding-right: 0px; padding-left: 0px; padding-top: 0px; padding-bottom: 5px;">
            <div style="font-size:12px;line-height:14px;color:#E15A5A;font-family:'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;text-align:left;">
            <p style="margin: 0;font-size: 12px;line-height: 14px;text-align: center">
                <span style="font-size: 18px; line-height: 21px;">
                <strong>
                    <span style="line-height: 21px; font-size: 18px;">Click the gift to get your special surprise!</span>
                </strong>
                </span>
            </p>
            </div>
        </div>
        <!--[if mso]></td></tr></table><![endif]-->
        </div>

        <div class="">
        <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 30px;"><![endif]-->
        <div style="color:#989898;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;line-height:120%; padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 30px;">
            <div style="font-size:12px;line-height:14px;color:#989898;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
            <p style="margin: 0;font-size: 14px;line-height: 17px;text-align: center">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eu ullamcorper tellus. Nulla
                eu lacinia metus. Duis tempor dictum tortor a ultricies. Donec interdum neque quis lacus porta,
                a varius dui iaculis.</p>
            </div>
        </div>
        <!--[if mso]></td></tr></table><![endif]-->
        </div>

        <!--[if (!mso)&(!IE)]><!-->
    </div>
"""


api_test_bp = Blueprint('api_test', __name__)
api_test = Api(api_test_bp)
api_test.add_resource(TestEmail, '/v2/test/email')
