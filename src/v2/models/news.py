from ..modules.db import connection
from .users import Users
from sqlalchemy import Table, Column, MetaData, select, func, desc, BIGINT, VARCHAR, DATETIME, Enum, TEXT, or_

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
             Column('updated_at', TEXT),
             Column('draft', TEXT)
             )

join_user = News.join(Users, News.c.author == Users.c.id_user)

# ref: http://docs.sqlalchemy.org/en/latest/core/expression_api.html?highlight=label#sqlalchemy.sql.expression.label
select_column = [News.c.id, News.c.title, News.c.content, News.c.status, News.c.image,
                 News.c.tag, News.c.tag, News.c.created_at, News.c.updated_at, News.c.draft,
                 Users.c.username, Users.c.id_user, Users.c.moto, Users.c.avatar]


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

    if 'status' in Params:
        if 'draft' in Params['status']:
            s = s.where(News.c.status == 'draft')
            c = c.where(News.c.status == 'draft')
        if 'published' in Params['status']:
            s = s.where(News.c.status == 'post')
            c = c.where(News.c.status == 'post')

    if 'tag' in Params:
        s = s.where(News.c.tag.like('%'+Params['tag']+'%'))
        c = c.where(News.c.tag.like('%'+Params['tag']+'%'))

    # show draf news
    if "show_draft" not in Params or Params["show_draft"] == False:
        s = s.where(or_(News.c.draft != "1", News.c.draft == None))
        c = c.where(or_(News.c.draft != "1", News.c.draft == None))

    if "draft" in Params:
        if Params["draft"] == True:
            s = s.where(or_(News.c.draft == "1"))
            c = c.where(or_(News.c.draft == "1"))
        else:
            s = s.where(or_(News.c.draft != "1"))
            c = c.where(or_(News.c.draft != "1"))

    res = connection.execute(s)
    rescount = connection.execute(c)

    return {
        'data': res.fetchall(),
        'count': rescount.fetchone()['total']
    }

# model to update news by news id


def updateNews(Params, id):
    query = News.update().where(News.c.id == id).values(Params)
    return connection.execute(query)


def createNews(Params):
    query = News.insert().values(Params)
    return connection.execute(query)


def getDetail(id):
    s = select(select_column).select_from(join_user).where(News.c.id == id)
    res = connection.execute(s)
    row = res.fetchone()
    if not row:
        return {}
    else:
        return row
