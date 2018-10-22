import os
import datetime
import json
import hashlib
from flask import Blueprint, request
from flask_restful import Api, Resource
from v2.modules.file_upload import handleUpload
from v2.helpers.response import apiResponse
from v2.models.users import login, oauthLogin, checkUsername, checkEmail, register
from v2.transformers.user import transform
from wtforms import Form, BooleanField, StringField, PasswordField, validators, FileField


class RegiterFormValidator(Form):
    username = StringField('Username', [validators.Length(min=4, max=100)])
    email = StringField('Email', [validators.Length(min=4, max=50)])
    password = StringField('Nama lengkap', [validators.Length(min=4, max=100)])
    avatar = FileField('avatar')


class Login(Resource):
    def post(self):
        # ref md5 hash: https://stackoverflow.com/a/5297495/2780875
        params = {
            'username': request.form.get('username'),
            'password': hashlib.md5(request.form.get('password')).hexdigest()
        }

        result = login(params)
        if result is not None:
            return apiResponse(200,  'Login berhasil', {'data': transform(result)})
        else:
            return apiResponse(204)


class Register(Resource):
    def post(self):

        form = RegiterFormValidator(request.form)
        if form.validate():
            # validation is valid
            # set params value
            params = {
                'username': request.form.get('username'),
                'fullname': request.form.get('fullname'),
                'password': request.form.get('password'),
                'email': request.form.get('email'),
                'fullname': request.form.get('fullname'),
            }

            if params["fullname"] is None:
                params["fullname"] = ""

            # set default params

            message = ''

            # check if user with same username
            resCheckUsername = checkUsername(params['username'])
            resCheckEmail = checkEmail(params['email'])

            # generate validation message
            if resCheckUsername is not None:
                message += 'username telah terpakai, silahkan menggunakan yang lain. '
            if resCheckEmail is not None:
                message += 'email telah terpakai, silahkan menggunakan yang lain'

            # is not valid
            if len(message) > 0:
                return apiResponse(400, message), 400
            else:
                # upload avatar
                upload_dir_db = '/' + params["username"] + '/avatar/'
                upload_dir = os.environ.get(
                    'MEDIA_DIR', '../media-kompetisiid') + upload_dir_db
                input_avatar = request.files['avatar']
                avatar = handleUpload(upload_dir, input_avatar, upload_dir_db)

                # set params["avatar"] value
                params["avatar"] = json.dumps(avatar, separators=(',', ':'))
                userdata = register(params)
                return apiResponse(201, "Registrasi berhasil, selamat datang " + params["username"], {"data": userdata}), 201
        else:
            return apiResponse(400, 'formdata not valid'), 400


class OauthLogin(Resource):
    def post(self):
        params = {
            'provider': request.form.get('provider'),
            'user_id': request.form.get('user_id')
        }

        result = oauthLogin(params)
        if result is not None:
            return apiResponse(200,  'Login berhasil', {'data': transform(result)})
        else:
            return apiResponse(204, 'Akun tidak ditemukan, silahkan melakukan "registrasi" terlebih dahulu')


api_auth_bp = Blueprint('api_auth', __name__)
api_auth = Api(api_auth_bp)
api_auth.add_resource(Login, '/v2/login')
api_auth.add_resource(Register, '/v2/register')
api_auth.add_resource(OauthLogin, '/v2/oauth/login')
