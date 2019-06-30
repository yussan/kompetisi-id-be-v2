from flask import Blueprint, request
from flask_restful import Resource, Api
from ..models.news import getDetail, getList, updateNews
from ..helpers.encId import decId
from ..helpers.response import apiResponse
from ..transformers.news import transform
from ..helpers.encId import decId
from ..models.users import getDataByUserKey
from ..modules.file_upload import handleUpload
from wtforms import Form, StringField, TextAreaField, validators

import json 
import os
import datetime

class CreateNewsValidator(Form):
    title = StringField("Judul Berita", [validators.required(), validators.length(min=4, max=100)])
    content = TextAreaField("Konten", [validators.required(), validators.length(min=4, max=5000)])
    tags = StringField("Tags", [validators.required(), validators.length(min=4, max=2000)])

class News(Resource):
    # controller to get news bew news id
    def get(self, encid):
        # decrypt id
        id = decId(encid)
        data = getDetail(id)

        if(data):
            # get related post
            ParamsRelated = {"status": ["published"], "notid": id, "limit": 3}
            related = getList(ParamsRelated)
            relateddata = []
            for n in related["data"]:
                relateddata.append(transform(n))

            return apiResponse(200, "success", {"data": dict(transform(data)), "related": relateddata}), 200
        else:
            return apiResponse(204, "berita tidak ditemukan"), 200

    # controller to update news by news id
    def put(self, encid):
        id = decId(encid)

        news = getDetail(id)

        if(news):
            # check userkey
            userkey = request.headers.get('User-Key')
            if userkey is None:
                # user not valid
                return apiResponse(403, "kamu tidak memiliki akses disini"), 403
            else:
                userdata = getDataByUserKey(userkey)
                if userdata is None:
                    return apiResponse(403, "kamu tidak memiliki akses disini"), 403
                else:
                    # form validation
                    form = CreateNewsValidator(request.form)

                    if form.validate():
                      # form is valid and ready to the mysql query
                      params = {} 
                      # get current timestamp
                      now = datetime.datetime.now()

                      # check is upload new image
                      if "image" in request.files:
                          upload_dir_db = '/news/' + userdata["username"] + '/'+ str(now.year)
                          upload_dir = os.environ.get(
                              'MEDIA_DIR', '../media-kompetisiid') + upload_dir_db
                          input_poster = request.files['image']
                          poster = handleUpload(upload_dir, input_poster, upload_dir_db)
                          # return as json stringify
                          params["image"] = json.dumps(poster)

                      params["title"] = request.form.get("title")
                      params["content"] = request.form.get("content")
                      params["tag"] = request.form.get("tags")
                      params["updated_at"] = now.strftime('%Y-%m-%d %H:%M:%S')
                      params["draft"] = "1" if request.form.get("draft") == "true" else "0"

                      # start update query
                      updateNews(params, id)

                      return apiResponse(200, "berita update berita"), 200
                    else:
                      # form is not valid
                      # convert error message to string
                      error_messages = ""
                      for key, val in form.errors.items():
                          error_messages += key + ": " + val[0] + " "
                          
                      # get validation error message
                      return apiResponse(400, error_messages), 400
        else:
            return apiResponse(204, "berita tidak ditemukan"), 200

    # controller to delete news by news id
    def delete(self, encid):
        return {}, 201


api_news_bp = Blueprint("api_news", __name__)
api_news = Api(api_news_bp)
api_news.add_resource(News, "/v2/news/<string:encid>")
