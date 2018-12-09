from flask import Blueprint, request
from flask_restful import Api, Resource
from ..helpers.encId import decId
from ..models.competitions import getDetail, insertData, updateData
from ..models.users import getDataByUserKey
from ..transformers.competition import transform
from ..helpers.response import apiResponse
from wtforms import Form, StringField, TextAreaField, FileField, validators, BooleanField
from ..modules.file_upload import handleUpload

import datetime 
import os

# class to validate post
class CreateCompetitionValidator(Form):
    title = StringField('Judul kompetisi', [
                        validators.required(), validators.Length(min=4, max=100)])
    description = TextAreaField('Deskripsi kompetisi', [
                                validators.required(), validators.Length(min=50, max=500)])
    prize_total = StringField('Total nilai hadiah', [validators.required()])
    prize_description = TextAreaField('Deskripsi hadiah', [
                                      validators.required(), validators.Length(max=2000)])
    organizer = StringField('Penyelenggara', [validators.required()])
    source_link = StringField('Link sumber', [validators.required()])
    # poster = FileField('Poster kompetisi', [validators.required()])
    tags = StringField('Tags', [validators.required()])
    content = TextAreaField('Detail kompetisi', [
                                       validators.required(), validators.Length(min=100, max=5000)])
    main_cat = StringField('Main kategori', [validators.required()])
    sub_cat = StringField('Sub kategori', [validators.required()])



class CompetitionApi(Resource):
    # controller to post new competition
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

        # validation form data
        form = CreateCompetitionValidator(request.form)
        if form.validate():
            params = {}
            # get current timestamp
            now = datetime.datetime.now()

            # handle upload poster
            if "poster" not in request.files:
                # get validation error message
                return apiResponse(400, "poster wajib diupload"), 400
            else: 
                # upload poster first
                upload_dir_db = '/' + userdata["username"] + '/poster/'+ str(now.year)
                upload_dir = os.environ.get(
                    'MEDIA_DIR', '../media-kompetisiid') + upload_dir_db
                input_poster = request.files['poster']
                poster = handleUpload(upload_dir, input_poster, upload_dir_db)
                # return as json stringify
                params["poster"] = str(poster)

            # set post status
            if userdata["level"] is "moderator" or userdata["level"] is "admin":
                params["status"] = "posted"
            else:
                params["status"] = "waiting" 

            # transform request to insert row data
            params["judul_kompetisi"] = request.form.get("title")
            params["sort"] = request.form.get("description") 
            params["penyelenggara"] = request.form.get("organizer")
            params["konten"] = request.form.get("content")
            params["created_at"] = now.strftime('%Y-%m-%d %H:%M:%S')
            params["updated_at"] = now.strftime('%Y-%m-%d %H:%M:%S')
            params["id_user"] = userdata["id_user"]
            params["id_main_kat"] = request.form.get("main_cat")
            params["id_sub_kat"] = request.form.get("sub_cat")
            params["deadline"] = request.form.get("deadline_date")
            params["pengumuman"] = request.form.get("announcement_date")
            params["total_hadiah"] = request.form.get("prize_total")
            params["hadiah"] = request.form.get("prize_description")
            params["tag"] = request.form.get("tags")
            params["rating"] = 0
            params["views"] = 0
            params["dataPengumuman"] = request.form.get("annoucements")
            params["dataGaleri"] = ""
            params["kontak"] = request.form.get("contacts")
            params["sumber"] =request.form.get("source_link")
            params["ikuti"] =request.form.get("register_link")
            params["mediapartner"] = 1 if request.form.get("is_mediapartner") is "true" else 0
            params["garansi"] = "1" if request.form.get("is_guaranteed") is "true" else "0"
            params["manage"] = "0"

            # insert into database competition table
            insertData(params)

            return apiResponse(201, "kompetisi berhasil di tambahkan"), 201
        else:
            # print form.errors
            # convert error message to string
            error_messages = ""
            for key, val in form.errors.items():
                error_messages += key + ": " + val[0] + " "
                
            # get validation error message
            return apiResponse(400, error_messages), 400


class CompetitionDetailApi(Resource):

    # controller to get competition by id
    def get(self, encid):
        id = decId(encid)
        competition = getDetail(id)

        if(competition['data'] != None):
            competition['data'] = transform(competition['data'])
            # competition found
            return apiResponse(200, 'success', competition), 200
        else:
            # component not found
            return apiResponse(204, 'Kompetisi tidak ditemukan'), 200

    # controller to update competition by id
    def put(self, encid):
        id = encid
        competition = getDetail(id)

        # check competition by id
        if(competition['data'] is not None):
            # check user key
            userkey = request.headers.get('User-Key')
            if userkey is None:
                return apiResponse(403, "anda tidak memiliki akses disini"), 403
            else:
                # check userkey on database
                userdata = getDataByUserKey(userkey)
                if userdata is None:
                    return apiResponse(403, "anda tidak memiliki akses disini"), 403
                else: 
                    # is author / moderator / admin 
                    if userdata["level"] == "moderator" or userdata["level"] == "admin" or userdata["id_user"] == competition["data"]["id_user"]:
                        # start update database
                        params = {}
                        # get current timestamp
                        now = datetime.datetime.now()

                        # handle update poster
                        if "poster" in request.files:
                            # upload poster first
                            upload_dir_db = '/' + userdata["username"] + '/poster/'+ str(now.year)
                            upload_dir = os.environ.get(
                                'MEDIA_DIR', '../media-kompetisiid') + upload_dir_db
                            input_poster = request.files['poster']
                            poster = handleUpload(upload_dir, input_poster, upload_dir_db)
                            # return as json stringify
                            params["poster"] = str(poster)
                            
                        # set post status
                        if userdata["level"] is "moderator" or userdata["level"] is "admin":
                            params["status"] = "posted"
                        else:
                            params["status"] = "waiting" 
                        
                        # transform request to insert row data
                        params["judul_kompetisi"] = request.form.get("title")
                        params["sort"] = request.form.get("description") 
                        params["penyelenggara"] = request.form.get("organizer")
                        params["konten"] = request.form.get("content")
                        params["updated_at"] = now.strftime('%Y-%m-%d %H:%M:%S')
                        params["id_main_kat"] = request.form.get("main_cat")
                        params["id_sub_kat"] = request.form.get("sub_cat")
                        params["deadline"] = request.form.get("deadline_date")
                        params["pengumuman"] = request.form.get("announcement_date")
                        params["total_hadiah"] = request.form.get("prize_total")
                        params["hadiah"] = request.form.get("prize_description")
                        params["tag"] = request.form.get("tags")
                        params["dataPengumuman"] = request.form.get("annoucements")
                        params["dataGaleri"] = ""
                        params["kontak"] = request.form.get("contacts")
                        params["sumber"] =request.form.get("source_link")
                        params["ikuti"] =request.form.get("register_link")
                        params["mediapartner"] = 1 if request.form.get("is_mediapartner") is "true" else 0
                        params["garansi"] = "1" if request.form.get("is_guaranteed") is "true" else "0"
                        params["manage"] = "0"

                        # insert into database competition table
                        updateData(params, id)
                        
                        return apiResponse(200, 'Kompetisi berhasil di update'), 200
                    else :
                        return apiResponse(403, "anda tidak memiliki akses disini"), 403
            
        else:
            # component not found
            return apiResponse(204, 'Kompetisi tidak ditemukan'), 200
        pass

    # competition to delete competition by id
    def delete(self, encid):
        pass

api_competition_detail_bp = Blueprint('api_competition_detail', __name__)
api_competition_detail = Api(api_competition_detail_bp)
api_competition_detail.add_resource(
    CompetitionDetailApi, '/v2/competition/<encid>')

api_competition_bp = Blueprint("api_competition", __name__)
api_competition = Api(api_competition_bp)
api_competition.add_resource(CompetitionApi, "/v2/competition")
