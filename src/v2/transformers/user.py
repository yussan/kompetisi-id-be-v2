import os
import json
import re


def transform(n):

    nextdata = {
        "id": n.id_user,
        "address": n.alamat,
        "fullname": n.fullname,
        "username": n.username,
        "email": n.email,
        "moto": n.moto,
        "status": n.status,
        "level": n.level,
        "is_verified": n.is_verified == 1,
        "is_banned": n.status == "banned",
        # ref: https://stackoverflow.com/a/50763403/2780875
        "register_date": n.tgl_gabung.strftime("%Y-%m-%d %H:%M:%S"),
        "user_key": n.user_key,
        "avatar": transformAvatar(n.avatar)
    }

    return nextdata


def transformAvatar(avatar):
    # generate avatar
    if not avatar:
        avatar = {
            "small": "/assets/4.2/img/avatar-default.jpg",
            "original": "/assets/4.2/img/avatar-default.jpg",
        }
    else:
        try:
            avatar = json.loads(avatar)
            avatar = {
                "small": avatar["small"] if avatar["small"].find("http") > -1 else os.environ.get("MEDIA_HOST", "https://media.kompetisi.id") + avatar["small"],
                "original": avatar["original"] if re.match(r"^http", avatar["original"]) else os.environ.get("MEDIA_HOST", "https://media.kompetisi.id") + avatar["original"]
            }
        except ValueError:
            avatar = {
                "small": "/assets/4.2/img/avatar-default.jpg",
                "original": "/assets/4.2/img/avatar-default.jpg",
            }

    return avatar
