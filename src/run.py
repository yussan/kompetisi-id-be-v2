from flask import Flask
from flask_restful import Api, Resource
from flask_json import json_response

app = Flask(__name__)
api = Api(app)

app.config['JSON_ADD_STATUS'] = False
app.config['JSON_DATETIME_FORMAT'] = '%d/%m/%Y %H:%M:%S'

# dummy data
competitions = [
    {'id': 1, 'title':'competition title 1', 'desc': 'this is short desc'},
    {'id': 2, 'title': 'competition title 2', 'desc': 'this is short desc'},
    {'id': 3, 'title': 'competition title 3', 'desc': 'this is short desc'},
]

# routes of user endpoint
class UserAPI(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

# routes of list competition endpoint
class CompetitionApi(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

# routes of list competition endpoint
class CompetitionListApi(Resource):
    def get(self):
        pass

    def post(self):
        pass

# handle 404
@app.errorhandler(404)
def pageNotFound(e):
    return json_response(status=404, message='endpoint tidak ditemukan')

# add endpoint to resource
api.add_resource(UserAPI, '/users/<int:id>', endpoint = 'user')
api.add_resource(CompetitionListApi, '/competition', endpoint = 'competitions')
api.add_resource(CompetitionApi, '/competition/<int:id>', endpoint = 'competition')

if __name__ == '__main__':
    app.run(debug=True, port=18081)
