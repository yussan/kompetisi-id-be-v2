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

select_column = [Users.c.id_user, Users.c.username, Users.c.email, Users.c.fullname, Users.c.moto, Users.c.last_login, Users.c.status, Users.c.level, Users.c.is_verified]

def login(params):
  query = select(select_column)\
    .select_from(Users)\
    .where(or_(Users.c.username == params['username'], Users.c.email == params['username']))\
    .where(Users.c.password == params['password'])

  result = connection.execute(query).fetchone()

  return result