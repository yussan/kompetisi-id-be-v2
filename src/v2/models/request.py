from ..modules.db import connection
from sqlalchemy import Table, Column, MetaData, select, update, insert, func, BIGINT, INT, DATETIME, TEXT, or_
import datetime

metadata = MetaData()

Request = Table('request', metadata,
                Column('id_req', BIGINT),
                Column('nama', TEXT),
                Column('email', TEXT),
                Column('link', TEXT),
                Column('poster', TEXT),
                Column('status', TEXT),
                Column('created_at', DATETIME),
                Column('updated_at', DATETIME),
                Column('accepted_at', DATETIME),
                Column('note', TEXT)
                )

select_column = [Request.c.id_req, Request.c.nama, Request.c.email, Request.c.link, Request.c.poster, Request.c.status,
                 Request.c.created_at, Request.c.updated_at, Request.c.accepted_at, Request.c.note]


def getRequest(Params={}):
    # order by
    orderby = Request.c.id_req.desc()

    s = select(select_column).order_by(orderby).select_from(Request)
    c = select([func.count().label('total')]).select_from(Request)

    # limit result
    if 'limit' in Params:
        s = s.limit(Params['limit'])
    else:
        s = s.limit(20)

    # filter by status
    if(Params['status'] in ['reject', 'waiting', 'posted']):
        print('status accepted')
        s = s.where(Request.c.status == Params['status'])
        c = c.where(Request.c.status == Params['status'])

    res = connection.execute(s)
    rescount = connection.execute(c)

    return {
        'data': res.fetchall(),
        'count': rescount.fetchone()['total']
    }

def insertRequest(Params={}):
    # ref: https://stackoverflow.com/a/13370382
    Params['created_at'] = datetime.datetime.utcnow()
    Params['updated_at'] = datetime.datetime.utcnow()
    return connection.execute(Request.insert(), Params)