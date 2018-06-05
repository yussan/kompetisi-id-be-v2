import os
import datetime
import json
from flask import Blueprint, request
from flask_restful import Resource, Api
from wtforms import Form, BooleanField, StringField, PasswordField, validators, FileField
# from flask_mail import Message
from v2.modules.file_upload import handleUpload
from v2.modules.mail import sendEmail
from v2.models.request import getRequest, getRequestById, insertRequest, updateRequest
from v2.helpers.response import apiResponse
from v2.transformers.request import transform
from v2.middlewares.auth import isModerator

# validations
# ref: http://flask.pocoo.org/docs/0.12/patterns/wtforms/
class FormValidator(Form):
    title = StringField('Judul kompetisi', [validators.Length(min=4, max=100)])
    email = StringField('Email', [validators.Length(min=4, max=50)])
    link = StringField('Link', [validators.Length(min=4, max=100)])
    poster = FileField('poster')

# constrollers
class FormActionValidator(Form):
    status = StringField('Status', [validators.Length(min=4, max=10)])
    message = StringField('Pesan', [validators.Length(min=4, max=300)])

class RequestApi(Resource):

    # function to get list request
    def get(self):
        Params = {}

        limit = request.args.get('limit')
        status = request.args.get('status')

        # parameter generator
        if(limit):
            Params['limit'] = limit
        if(status):
            Params['status'] = status

        requestdata = []
        result = getRequest(Params)
        for n in result['data']:
            requestdata.append(transform(n))

        return apiResponse(200, 'ok', {'data': requestdata, 'count': result['count']}), 200

    # function to add list request
    # TODO: validation input file
    def post(self):
        form = FormValidator(request.form)
        if form.validate():

            # handle upload poster
            # ref : https://stackoverflow.com/a/30071999
            now = datetime.datetime.now()
            upload_dir_db = '/request/' + str(now.year)
            upload_dir = os.environ.get('MEDIA_DIR', '../media-kompetisiid') + upload_dir_db
            input_poster = request.files['poster']
            poster = handleUpload(upload_dir, input_poster, upload_dir_db) 
            
            # start to insert database
            params = {
                'nama': request.form.get('title'),
                'email': request.form.get('email'),
                'link': request.form.get('link'),
                # ref: https://stackoverflow.com/a/46227888/2780875
                'poster': json.dumps(poster, separators=(',',':')),
                'status': 'waiting',
                'note': ''
            }

            # insert data
            insertRequest(params)

            # email thanks
            sendEmail('Terimakasih Telah Mengirim Kompetisi - kompetisi.id',
                  EmailThanksBody, [params['email']])

            return apiResponse(201, 'Kompetisi kamu akan dicek oleh moderator, status selanjutkan akan kami kirim via email'), 201
        else: 
            return apiResponse(400, 'formdata not valid'), 400

class RequestAction(Resource):

    @isModerator
    def put(self, id):

        # check si request available
        request_data = getRequestById(id)

        if request_data :
            
            request_data = transform(request_data)

            form = FormActionValidator(request.form)
            if form.validate():
                params = {
                    'note': request.form.get('message'),
                    # status is one of: "posted" , "reject"
                    'status': request.form.get('status')
                }

                # updata database
                updateRequest(params, id)

                # send email to users
                # msg = Message('Kompetisi ada Telah kami pasang', sender = 'noreply@kompetisi.id', recipients = [request_data['email']])
                # msg.body =   'This is email body'
                # mail.send(msg)
                
                # json response
                return apiResponse(200, 'Request berhasil di update'), 200
            else:
                return apiResponse(400, 'formdata not valid'), 400
        else:
            return apiResponse(204, 'data request tidak ditemukan'), 200

# blueprint initial
api_request_bp = Blueprint('api_request', __name__)
api_request = Api(api_request_bp)

# middlewares


# routes
api_request.add_resource(RequestApi, '/v2/request')
api_request.add_resource(RequestAction, '/v2/request/action/<int:id>')

EmailThanksBody = """
<div class="">
        <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 30px; padding-left: 30px; padding-top: 30px; padding-bottom: 15px;"><![endif]-->
        <div style="color:#555555;font-family:'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;line-height:120%; padding-right: 30px; padding-left: 30px; padding-top: 30px; padding-bottom: 15px;">
            <div style="font-family:Montserrat, 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;font-size:12px;line-height:14px;color:#555555;text-align:left;">
            <p style="margin: 0;font-size: 12px;line-height: 14px;text-align: center">
                <span style="font-size: 18px; line-height: 21px;">
                <strong>Terimakasih Telah Mengirim Kompetisi</strong>
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
            <p style="margin: 0;font-size: 14px;line-height: 17px;text-align: center">
                Kompetisi yang kamu pasang akan divalidasi oleh moderator, kamu akan menerima email balasan berupa status aksi untuk kompetisi ini.
            </p>
            </div>
        </div>
        <!--[if mso]></td></tr></table><![endif]-->
        </div>

        <!--[if (!mso)&(!IE)]><!-->
    </div>
"""

