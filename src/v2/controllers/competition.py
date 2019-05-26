from flask import Blueprint, request
from flask_restful import Api, Resource
from ..helpers.encId import decId
from ..models.competitions import getDetail, insertData, updateData, getSingleLatest
from ..models.users import getDataByUserKey
from ..transformers.competition import transform
from ..helpers.response import apiResponse
from wtforms import Form, StringField, TextAreaField, FileField, validators, BooleanField
from ..modules.file_upload import handleUpload
from ..modules.sebangsa import postToSebangsa
from ..config.sebangsa import SBS_API, SBS_COMMUNITY_ID, SBS_COMMUNITY_ROOM, SBS_NEWS_ROOM, SBS_PASSWORD, SBS_USERNAME

import datetime
import os
import json

# class to validate post
class CreateCompetitionValidator(Form):
    title = StringField('Judul kompetisi', [
                        validators.required(), validators.Length(min=4, max=100)])
    description = TextAreaField('Deskripsi kompetisi', [
                                validators.required(), validators.Length(min=50, max=500)])
    prize_total = StringField('Total nilai hadiah', [validators.required()])
    prize_description = TextAreaField('Deskripsi hadiah', [
                                      validators.required(), validators.Length(max=100000)])
    organizer = StringField('Penyelenggara', [validators.required()])
    source_link = StringField('Link sumber', [validators.required()])
    # poster = FileField('Poster kompetisi', [validators.required()])
    tags = StringField('Tags', [validators.required()])
    content = TextAreaField('Detail kompetisi', [
        validators.required(), validators.Length(min=100, max=500000)])
    main_cat = StringField('Main kategori', [validators.required()])
    sub_cat = StringField('Sub kategori', [validators.required()])

# class to manage endpoint competition list
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
                return apiResponse(403, "akun tidak diteumkan"), 403

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
                upload_dir_db = '/poster/' + \
                    userdata["username"] + '/' + str(now.year)
                upload_dir = os.environ.get(
                    'MEDIA_DIR', '../media-kompetisiid') + upload_dir_db
                input_poster = request.files['poster']
                poster = handleUpload(upload_dir, input_poster, upload_dir_db)
                # return as json stringify
                params["poster"] = json.dumps(poster)

            # set post status
            if userdata["level"] == "moderator" or userdata["level"] == "admin":
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
            params["sumber"] = request.form.get("source_link")
            params["ikuti"] = request.form.get("register_link")
            params["mediapartner"] = "1" if request.form.get(
                "is_mediapartner") == "true" else "0"
            params["garansi"] = "1" if request.form.get(
                "is_guaranteed") == "true" else "0"
            params["manage"] = "0"

            # insert into database competition table
            insertData(params)

            # get lattest data of competition
            latestCompetition = getSingleLatest()
            postUrl = "https://kompetisi.id/competition/" + \
                latestCompetition['id'] + "/regulations/" + latestCompetition['nospace_title'][0] + \
                " " + latestCompetition['title'] + \
                " #infokompetisi #kompetisiid"

            print("posturl", postUrl)

            # auto post to sebangsa
            postToSebangsa({
                "room_id": SBS_COMMUNITY_ROOM,
                "group_id": SBS_COMMUNITY_ID,
                "post": postUrl
            })

            return apiResponse(201, "kompetisi berhasil di tambahkan"), 201
        else:
            # print form.errors
            # convert error message to string
            error_messages = ""
            for key, val in form.errors.items():
                error_messages += key + ": " + val[0] + " "

            # get validation error message
            return apiResponse(400, error_messages), 400

# class to manage endpoint competition detail
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
        id = decId(encid)
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
                            upload_dir_db = '/poster/' + \
                                userdata["username"] + '/' + str(now.year)
                            upload_dir = os.environ.get(
                                'MEDIA_DIR', '../media-kompetisiid') + upload_dir_db
                            input_poster = request.files['poster']
                            poster = handleUpload(
                                upload_dir, input_poster, upload_dir_db)
                            # return as json stringify
                            params["poster"] = json.dumps(poster)

                        # set post status
                        if userdata["level"] == "moderator" or userdata["level"] == "admin":
                            params["status"] = request.form.get(
                                "status") if request.form.get("status") else "posted"
                        else:
                            params["status"] = "waiting"

                        # transform request to insert row data
                        params["judul_kompetisi"] = request.form.get("title")
                        params["sort"] = request.form.get("description")
                        params["penyelenggara"] = request.form.get("organizer")
                        params["konten"] = request.form.get("content")
                        params["updated_at"] = now.strftime(
                            '%Y-%m-%d %H:%M:%S')
                        params["id_main_kat"] = request.form.get("main_cat")
                        params["id_sub_kat"] = request.form.get("sub_cat")
                        params["deadline"] = request.form.get("deadline_date")
                        params["pengumuman"] = request.form.get(
                            "announcement_date")
                        params["total_hadiah"] = request.form.get(
                            "prize_total")
                        params["hadiah"] = request.form.get(
                            "prize_description")
                        params["tag"] = request.form.get("tags")
                        # params["dataPengumuman"] = request.form.get(
                        #     "annoucements")
                        params["dataGaleri"] = ""
                        params["kontak"] = request.form.get("contacts")
                        params["sumber"] = request.form.get("source_link")
                        params["ikuti"] = request.form.get("register_link")
                        params["mediapartner"] = "1" if request.form.get(
                            "is_mediapartner") == "true" else "0"
                        params["garansi"] = "1" if request.form.get(
                            "is_guaranteed") == "true" else "0"
                        params["manage"] = "0"

                        # update data pengumuman
                        # ref: http://strftime.org/
                        newAnnoucement = {"tgl": now.strftime(
                            '%Y-%m-%d %H:%M:%S'), "data": "Data kompetisi telah diupdate", "by": "sistem"}

                        if competition["data"]["dataPengumuman"] == "" or competition["data"]["dataPengumuman"] == None:
                            # create new pengumuman data
                            params["dataPengumuman"] = []
                        else:
                            # convert to array
                            params["dataPengumuman"] = json.loads(
                                competition["data"]["dataPengumuman"])

                        # push to data pengumuman from top
                        # ref : https://stackoverflow.com/a/17911209/2780875
                        params["dataPengumuman"].insert(0, newAnnoucement)

                        # convert array to string
                        params["dataPengumuman"] = json.dumps(
                            params["dataPengumuman"])

                        # insert into database competition table
                        print("updated competition", encid)
                        updateData(params, id)

                        return apiResponse(200, 'Kompetisi berhasil di update'), 200
                    else:
                        return apiResponse(403, "anda tidak memiliki akses disini"), 403

        else:
            # component not found
            return apiResponse(204, 'Kompetisi tidak ditemukan'), 200
        pass

    # competition to delete competition by id
    def delete(self, encid):
        pass

# class to manage endpoint competition announcemen
class CompetitionAnnouncement(Resource):
    def put(self, encid):

        userkey = request.headers.get('User-Key')

        if userkey == None:
            return apiResponse(403, "anda tidak memiliki akses disini"), 403
        else:
            # check userkey on database
            userdata = getDataByUserKey(userkey)
            if userdata is None:
                return apiResponse(403, "akun tidak ditemukan"), 403

        # userkey is valid
        userStatus = userdata.level if userdata.level != "user" else "penyelenggara"
        now = datetime.datetime.now()
        id = decId(encid)
        competition = getDetail(id)

        # check us competition available
        if(competition['data'] == None):
            return apiResponse(204, 'Kompetisi tidak ditemukan'), 200

        # only moderator, admin or author can added new annoucement
        if userdata["level"] == "moderator" or userdata["level"] == "admin" or userdata["id_user"] == competition["data"]["author"]["id"]:
            newAnnoucement = {"tgl": now.strftime(
                '%Y-%m-%d %H:%M:%S'), "data": request.form.get("pengumuman"), "by": userStatus}
            params = {}

            if competition["data"]["dataPengumuman"] == "" or competition["data"]["dataPengumuman"] == None:
                # create new pengumuman data
                params["dataPengumuman"] = []
            else:
                # convert to array
                params["dataPengumuman"] = json.loads(
                    competition["data"]["dataPengumuman"])

            params["dataPengumuman"].insert(0, newAnnoucement)
            params["dataPengumuman"] = json.dumps(params["dataPengumuman"])
            print("Added announcement", encid)
            updateData(params, id)

            return apiResponse(200, 'Pengumuman berhasil ditambahkan'), 200
        else:
            return apiResponse(403, "Anda tidak memiliki akses disini"), 403

    def delete(self, encid):
        # user key checker
        userkey = request.headers.get('User-Key')

        if userkey == None:
            return apiResponse(403, "anda tidak memiliki akses disini"), 403
        else:
            # check userkey on database
            userdata = getDataByUserKey(userkey)
            if userdata is None:
                return apiResponse(403, "akun tidak ditemukan"), 403

        # userkey is valid
        id = decId(encid)
        competition = getDetail(id)

        # check us competition available
        if(competition['data'] == None):
            return apiResponse(204, 'Kompetisi tidak ditemukan'), 200

        # only moderator, admin or author can added new annoucement
        if userdata["level"] == "moderator" or userdata["level"] == "admin" or userdata["id_user"] == competition["data"]["author"]["id"]:
            key = int(request.form.get("key"))
            params = {}
            params["dataPengumuman"] = json.loads(competition["data"]["dataPengumuman"])

            if params["dataPengumuman"] != "" and params["dataPengumuman"] != None and len(params["dataPengumuman"]) > key:
                # check is made by sistem or not
                if params["dataPengumuman"][key]["by"] == "sistem":
                    return apiResponse(422, 'Tidak bisa hapus pengumuman dari sistem'), 200
                
                # delete announcement by key
                params["dataPengumuman"].pop(key)

                # update announcement on database
                params["dataPengumuman"] = json.dumps(params["dataPengumuman"])
                updateData(params, id)
                return apiResponse(200, 'Pengumuman berhasil dihapus'), 200
            else:
                # pengumuman tidak ditemukan
                return apiResponse(422, "Pengumuman tidak ditemukan"), 200

            # params["dataPengumuman"].insert(0, newAnnoucement)
            # params["dataPengumuman"] = json.dumps(params["dataPengumuman"])
            # print("Added announcement", encid)
            # updateData(params, id)
        else:
            return apiResponse(403, "Anda tidak memiliki akses disini"), 403


# Blueprint config
api_competition_detail_bp = Blueprint('api_competition_detail', __name__)
# api_competition_bp = Blueprint("api_competition", __name__)

api_competition_detail = Api(api_competition_detail_bp)
# api_competition = Api(api_competition_bp)

api_competition_detail.add_resource(
    CompetitionDetailApi, '/v2/competition/<encid>')
api_competition_detail.add_resource(
    CompetitionAnnouncement, '/v2/competition/announcement/<encid>')
api_competition_detail.add_resource(CompetitionApi, "/v2/competition")
