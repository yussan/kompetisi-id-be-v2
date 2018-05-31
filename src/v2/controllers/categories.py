from flask import Blueprint, Request
from flask_restful import Api, Resource
from v2.models.categories import getMainCategories, getSubCategories
from v2.transformers.categories import transformMainCategory, transformSubCategory
from v2.helpers.response import api_response

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
      # get subcategories by main cat id
      subcategories = []
      for n in getSubCategories(mc['id']):
        sc = transformSubCategory(n)
        subcategories.append(sc)

      mc['subcategories'] = subcategories

      maincategories.append(mc)

    return api_response(200, 'ok', {'data': maincategories}), 200 

api_categories_bp = Blueprint('api_categories', __name__)
api_categories = Api(api_categories_bp)
api_categories.add_resource(MainCat, '/v2/maincategories')