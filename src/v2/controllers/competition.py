from flask import Blueprint, request
from flask_restful import Api, Resource
from v2.helpers.encId import decId
from v2.models.competitions import getDetail
from v2.transformers.competition import transform
from v2.helpers.response import apiResponse
from wtforms import Form, StringField, TextAreaField, FileField, validators, BooleanField


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
    competition_detail = TextAreaField('Detail kompetisi', [
                                       validators.required(), validators.Length(min=100, max=5000)])
    main_cat = StringField('Main kategori', [validators.required()])
    sub_cat = StringField('Sub kategori', [validators.required()])



class CompetitionApi(Resource):
    # controller to post new competition
    def post(self):
        # validation form data
        form = CreateCompetitionValidator(request.form)
        if form.validate():
            # handle upload poster
            


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
