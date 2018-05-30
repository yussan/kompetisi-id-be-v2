from flask import Blueprint, Request
from flask_restful import Api, Resource

api_category_bp = Blueprint('api_category', __name__)
api_category = Api(api_category_bp)

class MainCat(Resource):

  # function to get list all main categories
  def get(self):
    return {}

class SubCat(Resource):

  # function to get list sub categories by main category id
  def get(self, main_cat_id):
    return {}

api_category.add_resource(MainCat, '/v2/maincategories')
api_category.add_resource(SubCat, '/v2/subcategories/<int:main_cat_id>')