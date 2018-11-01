import datetime
import jwt

EMAIL_VERIFICATION_KEY = "FUCK_YOU_HACKER_FROM_KOMPETISIID"

# function to generate email token
# param {integer} id of user
# return {string} string of token
def generateEmailVerifToken(user_id):
  # generate token using jwt 
  # ref: https://realpython.com/token-based-authentication-with-flask/#encode-token
  payload = {
    "exp":  datetime.datetime.utcnow() + datetime.timedelta(days=0 , seconds=5),
    "iat": datetime.datetime.utcnow(),
    "sub": user_id
  } 

  return jwt.encode(
      payload,
      EMAIL_VERIFICATION_KEY,
      algorithm='HS256'
  )
  return user_id

# function to validation email token
# param {string} token get from email
# return {boolean}
def validationEmailVerifToken(user_id):
  return true