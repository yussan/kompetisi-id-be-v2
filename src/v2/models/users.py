from sqlalchemy import Table, Column, MetaData, join
from sqlalchemy import BIGINT, TEXT, VARCHAR

metadata = MetaData()
Users = Table('user', metadata,
              Column('id_user', BIGINT),
              Column('username', VARCHAR))