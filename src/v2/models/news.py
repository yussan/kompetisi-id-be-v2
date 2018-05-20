from ..modules.db import connect
from users import Users
from sqlalchemy import Table, Column, MetaData, select, func, desc, BIGINT, VARCHAR, DATETIME, Enum, TEXT

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


def getList(Params={}):

    # select data from table, order by id desc by default
    # ref: order by https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    s = select(select_column).order_by(News.c.id.desc()).select_from(join_user)

    # select total row from table
    c = select([func.count().label('total')]).select_from(join_user)

    # generate where
    if 'limit' in Params:
        s = s.limit(Params['limit'])
    if 'notid' in Params:
        s = s.where(News.c.id != Params['notid'])
        c = c.where(News.c.id != Params['notid'])
    if 'lastid' in Params:
        s = s.where(News.c.id < Params['lastid'])
    if 'draft' in Params['status']:
        s = s.where(News.c.status == 'draft')
        c = c.where(News.c.status == 'draft')
    if 'published' in Params['status']:
        s = s.where(News.c.status == 'post')
        c = c.where(News.c.status == 'post')
    if 'tag' in Params:
        s = s.where(News.c.tag.like('%'+Params['tag']+'%'))
        c = c.where(News.c.tag.like('%'+Params['tag']+'%'))

    res = connect.execute(s)
    rescount = connect.execute(c)

    return {
        'data': res.fetchall(),
        'count': rescount.fetchone()['total']
    }


def getDetail(id):
    s = select(select_column).where(News.c.id == id)
    res = connect.execute(s)
    row = res.fetchone()
    if not row:
        return {}
    else:
        return row
