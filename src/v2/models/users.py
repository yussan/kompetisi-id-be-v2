from ..modules.db import connection
import datetime
from sqlalchemy import Table, Column, MetaData, join
from sqlalchemy import BIGINT, INT, TEXT, VARCHAR, DATETIME, select, or_

metadata = MetaData()
Users = Table('user', metadata,
              Column('id_user', BIGINT),
              Column('username', VARCHAR),
              Column('email', VARCHAR),
              Column('fullname', VARCHAR),
              Column('moto', VARCHAR),
              Column('password', VARCHAR),
              Column('last_login', DATETIME),
              Column('status', TEXT),
              Column('level', TEXT),
              Column('is_verified', INT),
              )

UsersOauth = Table('user_oauth', metadata,
                  Column('id', BIGINT),
                  Column('user_id', BIGINT),
                  Column('provider', VARCHAR),
                  Column('oauth_user_id', VARCHAR),
                  Column('oauth_token', TEXT),
                  )

select_column_user = [Users.c.id_user, Users.c.username, Users.c.email, Users.c.fullname,
                 Users.c.moto, Users.c.last_login, Users.c.status, Users.c.level, Users.c.is_verified]

join_user = Users.join(UsersOauth, Users.c.id_user == UsersOauth.c.user_id)

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
    params['tgl_gabung'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    params['updated_at'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    params['last_login'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    print("register params", params)
    connection.execute(Users.insert(), params)

    # get last insert id
    last_id = connection.lastrowid

    print("last id", last_id)

    # return data from db 
    return {
        "username": params["username"]
    }

# function to select username by usrname and password
def login(params):
    query = select(select_column_user)\
        .select_from(Users)\
        .where(or_(Users.c.username == params['username'], Users.c.email == params['username']))\
        .where(Users.c.password == params['password'])

    result = connection.execute(query).fetchone()

    return result


def oauthLogin(params):
  query = select(select_column_user)\
        .select_from(join_user)\
        .where(UsersOauth.c.provider == params['provider'])\
        .where(UsersOauth.c.oauth_user_id == params['user_id'])

  result = connection.execute(query).fetchone()

  return result