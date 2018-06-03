import json
from flask import request
from v2.helpers.response import apiResponse

# only use and admin will valid
def isModerator(next_function):
  def wrapper(self, id):
    athorization = request.headers.get('Authorization')
    if athorization != 'yussan-1234567890' :
      return apiResponse(401, 'Not authorized'), 401
    else: 
      return next_function(self, id)
  return wrapper