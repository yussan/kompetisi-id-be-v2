from flask import Blueprint, request
from flask_restful import Api, Resource
from ..models.news import getList, createNews, updateNews
from ..helpers.response import apiResponse
from ..helpers.encId import decId
from ..transformers.news import transform
from ..models.users import getDataByUserKey
from ..modules.file_upload import handleUpload
from wtforms import Form, StringField, TextAreaField, validators

import datetime             
import json
import os

class CreateNewsValidator(Form):
    title = StringField("Judul Berita", [validators.required(), validators.length(min=4, max=100)])
    content = TextAreaField("Konten", [validators.required(), validators.length(min=4, max=5000)])
    tags = StringField("Tags", [validators.required(), validators.length(min=4, max=2000)])

class NewsList(Resource):
    # controller to get list news by some paramater
    def get(self):
        # get query
        limit = request.args.get('limit')
        lastid = request.args.get('lastid')
        notid = request.args.get('notid')
        status = request.args.get('status')
        tag = request.args.get('tag')

        if (not limit):
            limit = 9

        params = {
            'limit': limit
        }

        # get userkey on header and get userdata (optional)
        userkey = request.headers.get('User-Key')

        if userkey is not None:
            # get userdata by userkey
            # check userkey on database
            userdata = getDataByUserKey(userkey)

            if userdata is not None:
                show_draft = request.args.get('show_draft')
                params["show_draft"] = show_draft == "true" and (userdata["level"] == "admin" or userdata["level"] == "moderator")
                

        # custom params
        if (lastid):
            params['lastid'] = decId(lastid)
        if (tag):
            params['tag'] = tag
        if (status):
            # ref: https://docs.python.org/2/library/stdtypes.html#str.split
            params['status'] = status.split(',')
        else:
            params['status'] = []

        # get news list if id not
        if notid:
            params['notid'] = decId(notid)

        # get data from db
        news = getList(params)

        # return response as standard json
        if(len(news['data']) > 0):
            newsdata = []
            for n in news['data']:
                newsdata.append(transform(n))
            response = {}
            response['data'] = newsdata
            response['count'] = news['count']

            return apiResponse(200, 'success', response), 200
        else:
            return apiResponse(404, "berita tidak ditemukan"), 200

    # controller to post news
    def post(self):
        # check required header
        userkey = request.headers.get('User-Key')

        if userkey is None:
            return apiResponse(403, "anda tidak memiliki akses disini"), 403
        else:
            # check userkey on database
            userdata = getDataByUserKey(userkey)
            if userdata is None:
                return apiResponse(403, "anda tidak memiliki akses disini"), 403

        # form validation

        form = CreateNewsValidator(request.form)

        if form.validate():

          # image is required
          if "image" not in request.files:
            # get validation error message
            return apiResponse(400, "gambar wajib diupload"), 400
          else:
            params = {}
            # get current timestamp
            now = datetime.datetime.now()

            # process the image
            upload_dir_db = '/news/' + userdata["username"] + '/'+ str(now.year)
            upload_dir = os.environ.get(
                'MEDIA_DIR', '../media-kompetisiid') + upload_dir_db
            input_poster = request.files['image']
            poster = handleUpload(upload_dir, input_poster, upload_dir_db)
            # return as json stringify
            params["image"] = json.dumps(poster)

            # get formdata
            params["title"] = request.form.get("title")
            params["content"] = request.form.get("content")
            params["tag"] = request.form.get("tags")
            params["status"] = "post"
            params["author"] = userdata["id_user"]
            params["created_at"] = now.strftime('%Y-%m-%d %H:%M:%S')
            params["updated_at"] = now.strftime('%Y-%m-%d %H:%M:%S')
            params["draft"] = "1" if request.form.get("draft") == "true" else "0"

            # return params

            # insert to database
            createNews(params)

            return apiResponse(201, "berita berhasil di tambahkan"), 201
        else:
          # print form.errors
          # convert error message to string
          error_messages = ""
          for key, val in form.errors.items():
              error_messages += key + ": " + val[0] + " "
              
          # get validation error message
          return apiResponse(400, error_messages), 400


api_newslist_bp = Blueprint('api_newslist', __name__)
api_newslist = Api(api_newslist_bp)
api_newslist.add_resource(NewsList, '/v2/news')
