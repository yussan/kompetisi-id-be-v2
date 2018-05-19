from ..modules.db import connect
from users import Users
from sqlalchemy import Table, Column, MetaData, select, desc, BIGINT, VARCHAR, DATETIME, Enum, TEXT

metadata = MetaData()

# table declaration
News = Table('berita', metadata,
    Column('id', BIGINT),
    Column('title', VARCHAR),
    Column('image', TEXT),
    Column('tag', TEXT),
    Column('status', TEXT),
    Column('content', TEXT),
    Column('author', BIGINT),
    Column('created_at', TEXT),
    Column('updated_at', TEXT)
    )

join_user = News.join(Users, News.c.author == Users.c.id_user)

# ref: http://docs.sqlalchemy.org/en/latest/core/expression_api.html?highlight=label#sqlalchemy.sql.expression.label
select_column = [News.c.id, News.c.title, News.c.content, News.c.status, News.c.image, 
    News.c.tag, News.c.tag, News.c.created_at, News.c.updated_at,
    Users.c.username, Users.c.id_user]


def getList(Params = {}):

    data = []
    s = select(select_column)\
        .limit(Params['limit']).select_from(join_user)


    # generate where
    if 'lastid' in Params: s = s.where(News.c.id > Params['lastid'])
    if 'draft' in Params['status']: s = s.where(News.c.status == 'draft')
    if 'published' in Params['status']: s = s.where(News.c.status == 'post')

    res = connect.execute(s)
    rows = res.fetchall()

    return rows 

def getDetail(id):
    s = select(select_column).where(News.c.id == id)
    res = connect.execute(s)
    row = res.fetchone()
    if not row:
        return {}
    else:
        return row