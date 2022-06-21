from flask import Blueprint, request
from flask_restful import Api, Resource
from ..helpers.encId import decId
from ..transformers.competition import transform
from ..helpers.response import apiResponse
from wtforms import Form, StringField, TextAreaField, FileField, validators, BooleanField
from ..modules.file_upload import handleUpload
from ..modules.mail import sendEmail
# from ..modules.sebangsa import postToSebangsa
from ..config.sebangsa import SBS_API, SBS_COMMUNITY_ID, SBS_COMMUNITY_ROOM, SBS_NEWS_ROOM, SBS_PASSWORD, SBS_USERNAME

import datetime
import os
import json

# models
from ..models.competitions import getDetail, insertData, updateData, getSingleLatest, checkHaveLikedCompetition, getTotalActionCompetition
from ..models.users import getDataByUserKey
from ..models.competitions_subscription import checkHaveSubscribedCompetition

EmailReport = '''
    <div class=''>
            <!--[if mso]><table width='100%' cellpadding='0' cellspacing='0' border='0'><tr><td style='padding-right: 30px; padding-left: 30px; padding-top: 30px; padding-bottom: 15px;'><![endif]-->
            <div style='color:#555555;font-family:'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;line-height:120%; padding-right: 30px; padding-left: 30px; padding-top: 30px; padding-bottom: 15px;'>
                <div style='font-family:Montserrat, 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;font-size:12px;line-height:14px;color:#555555;text-align:left;'>
                <p style='margin: 0;font-size: 12px;line-height: 14px;text-align: center'>
                    <span style='font-size: 18px; line-height: 21px;'>
                    <strong>Ada Kiriman Kompetisi Baru</strong>
                    </span>
                </p>
                </div>
            </div>
            <!--[if mso]></td></tr></table><![endif]-->
            </div>

            <div class=''>
            <!--[if mso]><table width='100%' cellpadding='0' cellspacing='0' border='0'><tr><td style='padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 30px;'><![endif]-->
            <div style='color:#989898;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;line-height:120%; padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 30px;'>
                <div style='font-size:12px;line-height:14px;color:#989898;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;'>
                <p style='margin: 0;font-size: 14px;line-height: 17px;text-align: center'>
                    <a href='https://kompetisi.id/u/{}'>{}</a> baru saja memasang kompetisi berjudul '{}', silahkan cek di <a href='https://kompetisi.id/super/competition/waiting'>https://kompetisi.id/super/competition/waiting</a>
                </p>
                </div>
            </div>
            <!--[if mso]></td></tr></table><![endif]-->
            </div>

            <!--[if (!mso)&(!IE)]><!-->
        </div>
    '''

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
            return apiResponse(403, 'anda tidak memiliki akses disini'), 403
        else:
            # check userkey on database
            userdata = getDataByUserKey(userkey)
            if userdata is None:
                return apiResponse(403, 'akun tidak ditemukan'), 403

        # validation form data
        form = CreateCompetitionValidator(request.form)
        if form.validate():
            params = {}
            # get current timestamp
            now = datetime.datetime.now()

            # handle upload poster
            if 'poster' not in request.files:
                # get validation error message
                return apiResponse(400, 'poster wajib diupload'), 400
            else:
                # upload poster first
                upload_dir_db = '/poster/' + \
                    userdata['username'] + '/' + str(now.year)
                upload_dir = os.environ.get(
                    'MEDIA_DIR', '../media-kompetisiid') + upload_dir_db
                input_poster = request.files['poster']
                poster = handleUpload(upload_dir, input_poster, upload_dir_db)
                # return as json stringify
                params['poster'] = json.dumps(poster)

            # set post status
            if userdata['level'] == 'moderator' or userdata['level'] == 'admin':
                params['status'] = 'posted'
            else:
                params['status'] = 'waiting'

            # transform request to insert row data
            params['judul_kompetisi'] = request.form.get('title')
            params['sort'] = request.form.get('description')
            params['penyelenggara'] = request.form.get('organizer')
            params['konten'] = request.form.get('content')
            params['created_at'] = now.strftime('%Y-%m-%d %H:%M:%S')
            params['updated_at'] = now.strftime('%Y-%m-%d %H:%M:%S')
            params['id_user'] = userdata['id_user']
            params['id_main_kat'] = request.form.get('main_cat')
            params['id_sub_kat'] = request.form.get('sub_cat')
            params['deadline'] = request.form.get('deadline_date')
            params['pengumuman'] = request.form.get('announcement_date')
            params['total_hadiah'] = request.form.get('prize_total')
            params['hadiah'] = request.form.get('prize_description')
            params['tag'] = request.form.get('tags')
            params['rating'] = 0
            params['views'] = 0
            params['dataPengumuman'] = request.form.get('annoucements')
            params['dataGaleri'] = ''
            params['kontak'] = request.form.get('contacts')
            params['sumber'] = request.form.get('source_link')
            params['ikuti'] = request.form.get('register_link')
            params['mediapartner'] = '1' if request.form.get(
                'is_mediapartner') == 'true' else '0'
            params['garansi'] = '1' if request.form.get(
                'is_guaranteed') == 'true' else '0'
            params['manage'] = '0'
            params['draft'] = '1' if request.form.get(
                'draft') == 'true' else '0'

            # insert into database competition table
            insertData(params)

            # send report to moderator email

            # get lattest data of competition
            # latestCompetition = getSingleLatest()
            # postUrl = 'https://kompetisi.id/competition/' + \
            #     latestCompetition['id'] + '/regulations/' + latestCompetition['nospace_title'][0] + \
            #     ' ' + latestCompetition['title'] + \
            #     ' #infokompetisi #kompetisiid'

            # if params['status'] == 'posted' :
            #     # auto post to sebangsa
            #     postToSebangsa({
            #         'room_id': SBS_COMMUNITY_ROOM,
            #         'group_id': SBS_COMMUNITY_ID,
            #         'post': postUrl
            #     })

            body = EmailReport.format(
                userdata['username'], userdata['username'], params['judul_kompetisi'])

            # if member add create/update competition
            if userdata['level'] == 'user':
                sendEmail('Ada Kompetisi Baru Dipasang - kompetisi.id',
                          body, ['kompetisiindonesia@gmail.com'])

            return apiResponse(201, 'kompetisi berhasil di tambahkan'), 201
        else:
            # print form.errors
            # convert error message to string
            error_messages = ''
            for key, val in form.errors.items():
                error_messages += key + ': ' + val[0] + ' '

            # get validation error message
            return apiResponse(400, error_messages), 400

# class to manage endpoint competition detail


class CompetitionDetailApi(Resource):

    # controller to get competition by id
    def get(self, encid):
        id = decId(encid)

        # get headers data
        userkey = request.headers.get('User-Key')
        print("============userKey============ \n",  request.headers, "\n ===============================")

        # generate paramaters
        params = {
            'no_count': request.args.get('no_count') == '1'
        }

        competition = getDetail(id, params)

        if(competition['data'] != None):

            competition['data'] = transform(competition['data'])

            # get competition action stats
            actionStats = getTotalActionCompetition(id)
            competition['data']['stats']['likes'] = actionStats['likes']

            userdata = {}
            if userkey != None:
                userdata = getDataByUserKey(userkey)
                if userdata != None:
                    # check is liked competition
                    competition['data']['is_liked'] = checkHaveLikedCompetition(
                        {'competition_id': id, 'user_id': userdata['id_user'], 'onlyCheck': True})

                    # check is subsctibed competition
                    competition['data']['is_subscribed'] = checkHaveSubscribedCompetition(
                        {'competition_id': id, 'user_id': userdata['id_user']})
                else:
                    # default value
                    competition['data']['is_liked'] = False
                    competition['data']['is_subscribed'] = False
            else:
                competition['data']['is_liked'] = False

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
                return apiResponse(403, 'anda tidak memiliki akses disini'), 403
            else:
                # check userkey on database
                userdata = getDataByUserKey(userkey)
                if userdata is None:
                    return apiResponse(403, 'anda tidak memiliki akses disini'), 403
                else:
                    # is author / moderator / admin
                    if userdata['level'] == 'moderator' or userdata['level'] == 'admin' or userdata['id_user'] == competition['data']['id_user']:
                        # start update database
                        params = {}
                        # get current timestamp
                        now = datetime.datetime.now()

                        # handle update poster
                        if 'poster' in request.files:
                            # upload poster first
                            upload_dir_db = '/poster/' + \
                                userdata['username'] + '/' + str(now.year)
                            upload_dir = os.environ.get(
                                'MEDIA_DIR', '../media-kompetisiid') + upload_dir_db
                            input_poster = request.files['poster']
                            poster = handleUpload(
                                upload_dir, input_poster, upload_dir_db)
                            # return as json stringify
                            params['poster'] = json.dumps(poster)

                        # set post status
                        if userdata['level'] == 'moderator' or userdata['level'] == 'admin':
                            params['status'] = request.form.get(
                                'status') if request.form.get('status') else 'posted'
                        else:
                            params['status'] = 'waiting'

                        # transform request to insert row data
                        params['judul_kompetisi'] = request.form.get('title')
                        params['sort'] = request.form.get('description')
                        params['penyelenggara'] = request.form.get('organizer')
                        params['konten'] = request.form.get('content')
                        params['updated_at'] = now.strftime(
                            '%Y-%m-%d %H:%M:%S')
                        params['id_main_kat'] = request.form.get('main_cat')
                        params['id_sub_kat'] = request.form.get('sub_cat')
                        params['deadline'] = request.form.get('deadline_date')
                        params['pengumuman'] = request.form.get(
                            'announcement_date')
                        params['total_hadiah'] = request.form.get(
                            'prize_total')
                        params['hadiah'] = request.form.get(
                            'prize_description')
                        params['tag'] = request.form.get('tags')
                        # params['dataPengumuman'] = request.form.get(
                        #     'annoucements')
                        params['dataGaleri'] = ''
                        params['kontak'] = request.form.get('contacts')
                        params['sumber'] = request.form.get('source_link')
                        params['ikuti'] = request.form.get('register_link')
                        params['mediapartner'] = '1' if request.form.get(
                            'is_mediapartner') == 'true' else '0'
                        params['garansi'] = '1' if request.form.get(
                            'is_guaranteed') == 'true' else '0'
                        params['manage'] = '0'
                        params['draft'] = '1' if request.form.get(
                            'draft') == 'true' else '0'

                        # update data pengumuman
                        # ref: http://strftime.org/
                        newAnnoucement = {'tgl': now.strftime(
                            '%Y-%m-%d %H:%M:%S'), 'data': 'Data kompetisi telah diupdate', 'by': 'sistem'}

                        if competition['data']['dataPengumuman'] == '' or competition['data']['dataPengumuman'] == None:
                            # create new pengumuman data
                            params['dataPengumuman'] = []
                        else:
                            # convert to array
                            params['dataPengumuman'] = json.loads(
                                competition['data']['dataPengumuman'])

                        # push to data pengumuman from top
                        # ref : https://stackoverflow.com/a/17911209/2780875
                        params['dataPengumuman'].insert(0, newAnnoucement)

                        # convert array to string
                        params['dataPengumuman'] = json.dumps(
                            params['dataPengumuman'])

                        # insert into database competition table
                        updateData(params, id)

                        body = EmailReport.format(
                            userdata['username'], userdata['username'], params['judul_kompetisi'])

                        # if member add create/update competition
                        if userdata['level'] == 'user':
                            sendEmail('Ada Kompetisi Baru Dipasang - kompetisi.id',
                                      body, ['kompetisiindonesia@gmail.com'])

                        return apiResponse(200, 'Kompetisi berhasil di update'), 200
                    else:
                        return apiResponse(403, 'anda tidak memiliki akses disini'), 403

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
            return apiResponse(403, 'anda tidak memiliki akses disini'), 403
        else:
            # check userkey on database
            userdata = getDataByUserKey(userkey)
            if userdata is None:
                return apiResponse(403, 'akun tidak ditemukan'), 403

        # userkey is valid
        userStatus = userdata.level if userdata.level != 'user' else 'penyelenggara'
        now = datetime.datetime.now()
        id = decId(encid)
        competition = getDetail(id)

        # check us competition available
        if(competition['data'] == None):
            return apiResponse(204, 'Kompetisi tidak ditemukan'), 200

        # only moderator, admin or author can added new annoucement
        if userdata['level'] == 'moderator' or userdata['level'] == 'admin' or userdata['id_user'] == competition['data']['id_user']:
            newAnnoucement = {'tgl': now.strftime(
                '%Y-%m-%d %H:%M:%S'), 'data': request.form.get('pengumuman'), 'by': userStatus}
            params = {}

            if competition['data']['dataPengumuman'] == '' or competition['data']['dataPengumuman'] == None:
                # create new pengumuman data
                params['dataPengumuman'] = []
            else:
                # convert to array
                params['dataPengumuman'] = json.loads(
                    competition['data']['dataPengumuman'])

            params['dataPengumuman'].insert(0, newAnnoucement)
            params['dataPengumuman'] = json.dumps(params['dataPengumuman'])
            updateData(params, id)

            return apiResponse(200, 'Pengumuman berhasil ditambahkan'), 200
        else:
            return apiResponse(403, 'Anda tidak memiliki akses disini'), 403

    def delete(self, encid):
        # user key checker
        userkey = request.headers.get('User-Key')

        if userkey == None:
            return apiResponse(403, 'anda tidak memiliki akses disini'), 403
        else:
            # check userkey on database
            userdata = getDataByUserKey(userkey)
            if userdata is None:
                return apiResponse(403, 'akun tidak ditemukan'), 403

        # userkey is valid
        id = decId(encid)
        competition = getDetail(id)

        # check us competition available
        if(competition['data'] == None):
            return apiResponse(204, 'Kompetisi tidak ditemukan'), 200

        # only moderator, admin or author can added new annoucement
        if userdata['level'] == 'moderator' or userdata['level'] == 'admin' or userdata['id_user'] == competition['data']['author']['id']:
            key = int(request.form.get('key'))
            params = {}
            params['dataPengumuman'] = json.loads(
                competition['data']['dataPengumuman'])

            if params['dataPengumuman'] != '' and params['dataPengumuman'] != None and len(params['dataPengumuman']) > key:
                # check is made by sistem or not
                if params['dataPengumuman'][key]['by'] == 'sistem':
                    return apiResponse(422, 'Tidak bisa hapus pengumuman dari sistem'), 200

                # delete announcement by key
                params['dataPengumuman'].pop(key)

                # update announcement on database
                params['dataPengumuman'] = json.dumps(params['dataPengumuman'])
                updateData(params, id)
                return apiResponse(200, 'Pengumuman berhasil dihapus'), 200
            else:
                # pengumuman tidak ditemukan
                return apiResponse(422, 'Pengumuman tidak ditemukan'), 200

            # params['dataPengumuman'].insert(0, newAnnoucement)
            # params['dataPengumuman'] = json.dumps(params['dataPengumuman'])
            # updateData(params, id)
        else:
            return apiResponse(403, 'Anda tidak memiliki akses disini'), 403

# class to manage competition like action


class CompetitionLike(Resource):
    # like / unline competition by competition id and user key
    def post(self, encid):
        userkey = request.headers.get('User-Key')

        if userkey == None:
            return apiResponse(403, 'anda tidak memiliki akses disini'), 403
        else:
            # check userkey on database
            userdata = getDataByUserKey(userkey)
            if userdata is None:
                return apiResponse(403, 'akun tidak ditemukan'), 403

        # check is competition available
        id = decId(encid)
        competition = getDetail(id, {'no_count': True})

        if(competition['data'] == None):
            return apiResponse(204, 'Kompetisi tidak ditemukan'), 200

        # check is have liked competition
        haveLiked = checkHaveLikedCompetition(
            {'competition_id': id, 'user_id': userdata['id_user']})

        return {
            'liked': haveLiked
        }


# Blueprint config
api_competition_detail_bp = Blueprint('api_competition_detail', __name__)

api_competition_detail = Api(api_competition_detail_bp)

api_competition_detail.add_resource(
    CompetitionDetailApi, '/v2/competition/<encid>')
api_competition_detail.add_resource(
    CompetitionAnnouncement, '/v2/competition/announcement/<encid>')
api_competition_detail.add_resource(CompetitionApi, '/v2/competition')
api_competition_detail.add_resource(
    CompetitionLike, '/v2/competition/like/<encid>')
