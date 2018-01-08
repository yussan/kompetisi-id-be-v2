from ..modules.db import connect
from users import Users
from sqlalchemy import Table, Column, MetaData, select
from sqlalchemy import BIGINT, VARCHAR, DATETIME, Enum, TEXT

metadata = MetaData()

# table declaration
News = Table('berita', metadata,
             Column('id', BIGINT),
             Column('title', VARCHAR),
             Column('image', TEXT),
             Column('content', TEXT),
             Column('author', BIGINT)
             )

join_user = News.join(Users, News.c.author == Users.c.id)

def getData(Params = {}):
    data = []
    s = select([News.c.id, News.c.title, Users.c.username])\
        .limit(5).select_from(join_user)
    if(not Params.id != 0):
        s.where('')
    res = connect.execute(s)
    rows = res.fetchall()
    for n in rows:
        data.append(dict(n))
    print data

    return data