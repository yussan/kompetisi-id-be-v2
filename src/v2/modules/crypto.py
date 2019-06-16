import datetime
import jwt

EMAIL_VERIFICATION_KEY = "FUCK_YOU_HACKER_FROM_KOMPETISIID"

# function to generate email token
# param {integer} id of user
# return {string} string of token
def generateEmailVerifToken(user_id):
  # generate token using jwt 
  # ref: https://realpython.com/token-based-authentication-with-flask/#encode-token
  return generateKIToken(user_id, EMAIL_VERIFICATION_KEY)

  # payload = {
  #   "exp":  datetime.datetime.utcnow() + datetime.timedelta(days=7 , seconds=0),
  #   "iat": datetime.datetime.utcnow(),
  #   "sub": user_id
  # } 

  # return jwt.encode(
  #     payload,
  #     EMAIL_VERIFICATION_KEY,
  #     algorithm='HS256'
  # )

# function to get user id from email token
# param {string} token get from email
# return *
def validationEmailVerifToken(token):
  try:
    payload = jwt.decode(token, EMAIL_VERIFICATION_KEY)
    return int(payload["sub"])
  except jwt.ExpiredSignatureError:
    return 'Signature expired. Please log in again.'
  except jwt.InvalidTokenError:
    return 'Invalid token. Please log in again.'

# function to generate forgot password token
# params {string} sub data of stored
# return {string} string of token
def generateKIToken(sub, key):
  # generate token using jwt 
  # ref: https://realpython.com/token-based-authentication-with-flask/#encode-token
  payload = {
    "exp":  datetime.datetime.utcnow() + datetime.timedelta(days=7 , seconds=0),
    # "exp":  datetime.datetime.utcnow() + datetime.timedelta(minutes=1 , seconds=0),
    "iat": datetime.datetime.utcnow(),
    "sub": sub
  } 

  return jwt.encode(
    payload,
    key, 
    algorithm='HS256'
  )

def validationKIToken(token, key):
  try:
    payload = jwt.decode(token, key)
    return {
      "is_valid": True,
      "value": payload["sub"]
    }
  except jwt.ExpiredSignatureError:
    return {
      "is_valid": False,
      "message": "Token sudah tidak berlaku"
    }
  except jwt.InvalidTokenError:
    return {
      "is_valid": False,
      "message": "Token salah"
    }