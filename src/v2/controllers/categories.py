from flask import Blueprint, Request
from flask_restful import Api, Resource
from v2.models.categories import getMainCategories, getSubCategories
from v2.transformers.categories import transformMainCategory, transformSubCategory

api_category_bp = Blueprint('api_category', __name__)
api_category = Api(api_category_bp)

class MainCat(Resource):

  # function to get list all main categories
  def get(self):
    maincategories = []
    data = getMainCategories()
    for n in data:
      # transform main categories
      mc = transformMainCategory(n)
      mc['subcategories'] = []

      # get subcategories by main cat id
      subdata = getSubCategories(mc['id'])
      # transform sub categories
      for m in subdata:
        sc = transformSubCategory(m)
        mc['subcategories'].append(sc)

      maincategories.append(mc)
    return {'data': maincategories}

class SubCat(Resource):

  # function to get list sub categories by main category id
  def get(self, main_cat_id):
    return {}

api_category.add_resource(MainCat, '/v2/maincategories')
api_category.add_resource(SubCat, '/v2/subcategories/<int:main_cat_id>')