from ..modules.db import db
from flask import jsonify
from sqlalchemy import Table, Column, MetaData, select
from sqlalchemy import BIGINT, VARCHAR, DATETIME, Enum, TEXT

metadata = MetaData(bind=db)
conn = db.connect()
# table declaration
News = Table('berita', metadata,
             Column('id', BIGINT),
             Column('title', VARCHAR),
             Column('image', TEXT),
             Column('content', TEXT)
             )

def getData(Params = {}, id = 0):
    s = select([News.c.id, News.c.title]).limit(5)
    if(id != 0):
        s.where('')
    res = conn.execute(s)
    rows = res.fetchall()
    data = []
    for n in rows:
        data.append(dict(n))
    print data

    return data