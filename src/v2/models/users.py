from ..modules.db import connection
from ..modules.mail import sendEmail
from ..modules.crypto import generateEmailVerifToken
import datetime
import md5
from sqlalchemy import Table, Column, MetaData, join, outerjoin, BIGINT, INT, TEXT, VARCHAR, DATETIME, select, or_, update

metadata = MetaData()
Users = Table("user", metadata,
              Column("id_user", BIGINT),
              Column("username", VARCHAR),
              Column("avatar", TEXT),
              Column("email", VARCHAR),
              Column("fullname", VARCHAR),
              Column("moto", VARCHAR),
              Column("password", VARCHAR),
              Column("last_login", DATETIME),
              Column("tgl_gabung", DATETIME),
              Column("updated_at", DATETIME),
              Column("status", TEXT),
              Column("level", TEXT),
              Column("is_verified", INT),
              Column("gender", VARCHAR),
              Column("moto", VARCHAR),
              Column("user_key", TEXT)
              )

UsersOauth = Table("user_oauth", metadata,
                   Column("id", BIGINT),
                   Column("user_id", BIGINT),
                   Column("provider", VARCHAR),
                   Column("oauth_user_id", VARCHAR),
                   Column("oauth_token", TEXT),
                   )

select_column_user = [Users.c.id_user, Users.c.username, Users.c.email, Users.c.fullname,
                      Users.c.user_key, Users.c.avatar,
                      Users.c.moto, Users.c.tgl_gabung, Users.c.last_login, Users.c.status, Users.c.level, Users.c.is_verified]

join_user = Users.outerjoin(
    UsersOauth, Users.c.id_user == UsersOauth.c.user_id)

EmailVerificationBody = """
<div class="">
        <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 30px; padding-left: 30px; padding-top: 30px; padding-bottom: 15px;"><![endif]-->
        <div style="color:#555555;font-family:'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;line-height:120%; padding-right: 30px; padding-left: 30px; padding-top: 30px; padding-bottom: 15px;">
            <div style="font-family:Montserrat, 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;font-size:12px;line-height:14px;color:#555555;text-align:left;">
            <p style="margin: 0;font-size: 12px;line-height: 14px;text-align: center">
                <span style="font-size: 18px; line-height: 21px;">
                <strong>Terimakasih telah melakukan registrasi di Kompetisi Id</strong>
                </span>
            </p>
            </div>
        </div>
        <!--[if mso]></td></tr></table><![endif]-->
        </div>

        <div class="">
        <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 30px;"><![endif]-->
        <div style="color:#989898;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;line-height:120%; padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 30px;">
            <div style="font-size:12px;line-height:14px;color:#989898;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
            <p style="margin: 0;font-size: 14px;line-height: 17px;text-align: center">
                Masih ada satu langkah lagi sebelum memulai, silahkan konfirmasi email anda dengan klik <a href="{}" target="_blank">Link Berikut</a>
                <br/>
                Jika link tersebut tidak bekerja, silahkan buka link berikut ini 
                {}
            </p>
            </div>
        </div>
        <!--[if mso]></td></tr></table><![endif]-->
        </div>

        <!--[if (!mso)&(!IE)]><!-->
    </div>
"""

# function to get userdata by user id


def getDataById(userid):
    query = select(select_column_user)\
        .select_from(join_user)\
        .where(Users.c.id_user == userid)

    return connection.execute(query).fetchone()

def getDataByUserKey(userkey):
    query = select(select_column_user)\
        .select_from(join_user)\
        .where(Users.c.user_key == userkey)

    return connection.execute(query).fetchone()


def getDataByUsername(username):
    query = select(select_column_user)\
        .select_from(join_user)\
        .where(Users.c.username == username)

    return connection.execute(query).fetchone()

# function to check is available same username in table user


def checkUsername(username):
    query = select([Users.c.id_user])\
        .select_from(Users)\
        .where(Users.c.username == username)

    return connection.execute(query).fetchone()

# function to check is availbale same email in table user


def checkEmail(email):
    query = select([Users.c.id_user])\
        .select_from(Users)\
        .where(Users.c.email == email)

    return connection.execute(query).fetchone()

# function to insert data new user by register params


def register(params):
    # insert data to the db
    # ref: http://strftime.org/

    # ref: http://flask.pocoo.org/snippets/37/
    # cur = connection.db.cursor()

    password = md5.new()
    password.update(params["password"])

    current_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    params["tgl_gabung"] = current_date
    params["updated_at"] = current_date
    params["last_login"] = current_date
    params["is_verified"] = 0
    params["status"] = "active"
    params["gender"] = "-"
    params["moto"] = "-"
    params["password"] = password.hexdigest()
    params["level"] = "user"

    print("register params", params)
    print(connection.execute(Users.insert(), params))
    # connection.execute(Users.insert(), params)

    # get latest inserted user
    query = select(select_column_user)\
        .select_from(Users)\
        .order_by(Users.c.id_user.desc())

    user = connection.execute(query).fetchone()

    # send email confirmation to new user
    emailVerifToken = generateEmailVerifToken(user["id_user"])
    emailVerifUrl = "https://kompetisi.id/email-verification/" + emailVerifToken
    emailBody = EmailVerificationBody.format(emailVerifUrl, emailVerifUrl)
    sendEmail("Konfirmasi email anda untuk Kompetisi Id",
              emailBody, [params["email"]])

    return user


# function to select username by username and password
def login(params):
    query = select(select_column_user)\
        .select_from(Users)\
        .where(or_(Users.c.username == params["username"], Users.c.email == params["username"]))\
        .where(Users.c.password == params["password"])

    result = connection.execute(query).fetchone()

    return result

# function to set user email is valid


def setValidEmail(userId):
    query = update(Users).where(Users.c.id_user == userId).values(
        is_verified=1, updated_at=datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
    return connection.execute(query)

# function to update database


def updateData(Params, UserId):
    query = Users.update().where(Users.c.id_user == UserId).values(Params)
    return connection.execute(query)


def oauthLogin(params):
    query = select(select_column_user)\
        .select_from(join_user)\
        .where(UsersOauth.c.provider == params["provider"])\
        .where(UsersOauth.c.oauth_user_id == params["user_id"])

    result = connection.execute(query).fetchone()

    return result
