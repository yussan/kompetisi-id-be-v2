from ..modules.db import db
from sqlalchemy import Table, Column, MetaData, join
from sqlalchemy import BIGINT, TEXT, VARCHAR

metadata = MetaData(bind=db)
Users = Table('user', metadata,
              Column('id', BIGINT),
              Column('username', VARCHAR))