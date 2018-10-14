from ..modules.db import connection
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