import time
import hashlib
import requests
import json
from ..config.sebangsa import SBS_API, SBS_COMMUNITY_ID, SBS_PASSWORD, SBS_USERNAME

# function to return epoch time


def getTimestamp():
    return int(time.time())

# function to generate seal of Sebangsa


def generateSeal(path):
    timestamp = str(getTimestamp())
    seal = hashlib.md5(timestamp + "saltnyaapa" + path).hexdigest()
    return {
        "timestamp": timestamp,
        "seal": seal
    }

# function to post to sebangsa
def postToSebangsa(params={}):
    # request to Sebangsa Api
    # ref: http://trac.sebangsa.net/wiki/API/Core/NewPostEditor/CreateNewPOST
    loginSeal = generateSeal("user")
    postSeal = generateSeal("post")

    # request to Sebangsa Api

    # login to get key
    # ref: http://trac.sebangsa.net/wiki/API/Core/Login/Login
    loginUrl = SBS_API + "/user/" + \
        loginSeal["timestamp"] + "/" + loginSeal["seal"] + "/login"
    reqLogin = requests.post(loginUrl, data={
        "username": SBS_USERNAME, "password": hashlib.md5(SBS_PASSWORD).hexdigest()})
    resLogin = json.loads(reqLogin.text)

    # ref : http://trac.sebangsa.net/wiki/API/Core/NewPostEditor/CreateNewPOST
    postUrl = SBS_API + "/post/create/" + \
        postSeal["timestamp"] + "/" + \
        postSeal["seal"] + "/" + resLogin["user_key"]
    reqPost = requests.post(postUrl, data=params)
