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

join_user = News.join(Users, News.c.author == Users.c.id_user)

select_column = [News.c.id, News.c.title, Users.c.username]

def getList(Params = {}):
    data = []
    s = select(select_column)\
        .limit(Params['limit']).select_from(join_user)
    res = connect.execute(s)
    rows = res.fetchall()
    for n in rows:
        data.append(dict(n))

    return data

def getDetail(id):
    s = select(select_column).where(News.c.id == id)
    res = connect.execute(s)
    row = res.fetchone()
    print(row)
    if not row:
        return {}
    else:
        return dict(row)