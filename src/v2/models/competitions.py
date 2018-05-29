from ..modules.db import connection
import datetime
from v2.helpers.encId import encId
from v2.helpers.strings import generateTitleUrl
from users import Users
from sqlalchemy import Table, Column, MetaData, select, update, func, BIGINT, INT, DATETIME, TEXT, or_

metadata = MetaData()

# main category table declaration
MainCategory = Table('main_kat', metadata,
                     Column('id_main_kat', BIGINT),
                     Column('main_kat', TEXT),
                     Column('color', TEXT),
                     Column('logo', TEXT),
                     Column('deskripsi', TEXT)
                     )

# sub category table declaration
SubCategory = Table('sub_kat', metadata,
                    Column('id_sub_kat', BIGINT),
                    Column('sub_kat', TEXT)
                    )

# competition table delaration
Competition = Table('kompetisi', metadata,
                    Column('id_kompetisi', BIGINT),
                    Column('id_user', BIGINT),
                    Column('judul_kompetisi', TEXT),
                    Column('sort', TEXT),
                    Column('poster', TEXT),
                    Column('penyelenggara', TEXT),
                    Column('konten', TEXT),
                    Column('created_at', DATETIME),
                    Column('updated_at', DATETIME),
                    Column('deadline', DATETIME),
                    Column('pengumuman', DATETIME),
                    Column('total_hadiah', INT),
                    Column('hadiah', TEXT),
                    Column('tag', TEXT),
                    Column('status', TEXT),
                    Column('rating', INT),
                    Column('views', INT),
                    Column('mediapartner', INT),
                    Column('garansi', INT),
                    Column('dataPengumuman', TEXT),
                    Column('kontak', TEXT),
                    Column('sumber', TEXT),
                    Column('ikuti', TEXT),
                    Column('id_main_kat', INT),
                    Column('id_sub_kat', INT),
                    )

join_user = Competition.join(Users, Competition.c.id_user == Users.c.id_user)
join_main_cat = join_user.join(
    MainCategory, Competition.c.id_main_kat == MainCategory.c.id_main_kat)
join_sub_cat = join_main_cat.join(
    SubCategory, Competition.c.id_sub_kat == SubCategory.c.id_sub_kat)

select_column = [Competition.c.id_kompetisi, Competition.c.judul_kompetisi, Competition.c.sort, Competition.c.poster,
                 Competition.c.penyelenggara,
                 Competition.c.hadiah, Competition.c.total_hadiah,
                 Competition.c.konten, Competition.c.sumber, Competition.c.ikuti,
                 Competition.c.dataPengumuman,
                 Competition.c.created_at, Competition.c.updated_at, Competition.c.deadline, Competition.c.pengumuman,
                 Competition.c.tag, Competition.c.hadiah, Competition.c.status, Competition.c.rating,
                 Competition.c.views,
                 Competition.c.mediapartner, Competition.c.garansi,
                 Competition.c.kontak, Competition.c.sumber,
                 MainCategory.c.id_main_kat, MainCategory.c.main_kat,
                 SubCategory.c.id_sub_kat, SubCategory.c.sub_kat,
                 Users.c.username, Users.c.fullname, Users.c.moto]


def getList(Params={}):
    # order by
    orderby = Competition.c.id_kompetisi.desc()
    if 'orderby' in Params:
        if Params['orderby'] == 'prize_dsc':
            orderby = Competition.c.total_hadiah.desc()
    
    if Params['is_popular']:
        orderby = Competition.c.views.desc()

    # generate query to get data
    s = select(select_column).order_by(orderby).select_from(join_sub_cat)

    # generate query to get count
    c = select([func.count().label('total')]).select_from(Competition)

    # limit result
    if 'limit' in Params:
        s = s.limit(Params['limit'])

    # filter result by id
    if 'lastid' in Params:
        if 'orderby' in Params:
            if Params['orderby'] == 'prize_dsc':
                s = s.where(Competition.c.total_hadiah < Params['lastid'])
        else:
            s = s.where(Competition.c.id_kompetisi < Params['lastid'])

    # filter result by hashtag
    if 'tag' in Params:
        s = s.where(Competition.c.tag.like('%' + Params['tag'] + '%'))
        c = c.where(Competition.c.tag.like('%' + Params['tag'] + '%'))

    # filter result by search keyword based on title and tag
    if 'search' in Params:
        # ref _or: http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.or_
        s = s.where(or_(Competition.c.judul_kompetisi.like(
            '%' + Params['search'] + '%'), Competition.c.tag.like('%' + Params['search'] + '%')))
        c = c.where(or_(Competition.c.judul_kompetisi.like(
            '%' + Params['search'] + '%'), Competition.c.tag.like('%' + Params['search'] + '%')))

    # filter result by main kategori
    if 'mainkat' in Params:
        s = s.where(MainCategory.c.main_kat == Params['mainkat'])
        c = c.where(MainCategory.c.main_kat == Params['mainkat'])

    # filter result by sub kategori
    if 'subkat' in Params:
        s = s.where(SubCategory.c.sub_kat == Params['subkat'])
        c = c.where(SubCategory.c.sub_kat == Params['subkat'])

    # filter by status
    if 'status' in Params:
        if Params['status'] == 'active':
            s = s.where(Competition.c.deadline > datetime.datetime.now())
            c = c.where(Competition.c.deadline > datetime.datetime.now())

    # show mediapartner
    if Params['is_mediapartner']:
        s = s.where(Competition.c.mediapartner == 1)
        c = c.where(Competition.c.mediapartner == 1)

    # show guaranted competition
    if Params['is_guaranted']:
        s = s.where(Competition.c.garansi == "1")
        c = c.where(Competition.c.garansi == "1")

    # show popular competition
    if Params['is_popular']:
        s = s.where(or_(Competition.c.views > 50, Competition.c.views < 700))
        c = c.where(or_(Competition.c.views > 50, Competition.c.views < 700))

    res = connection.execute(s)
    rescount = connection.execute(c)

    return {
        'data': res.fetchall(),
        'count': rescount.fetchone()['total']
    }


def getRelated(id):
    #get detail competitoin 
    c_query = select([Competition.c.id_main_kat.label('main_kat'), Competition.c.tag]).select_from(Competition).where(Competition.c.id_kompetisi == id)
    competition  = connection.execute(c_query).fetchone()

    # get competition by main category
    s = select(select_column).order_by(
        Competition.c.id_kompetisi.desc()).select_from(join_sub_cat)\
        .where(MainCategory.c.main_kat == competition['main_kat'])\
        .where(Competition.c.deadline > datetime.datetime.now())\
        .where(Competition.c.id_kompetisi != id)\
        .limit(3)
    
    # generate query to get data
    res = connection.execute(s)
    data = res.fetchall()
    totaldata = len(data)

    if totaldata > 2:
        return {
            'data': data
        }
    else:
        s2 = select(select_column).order_by(
            Competition.c.id_kompetisi.desc()).select_from(join_sub_cat).limit(3 - totaldata)
        s2 = s2.where(Competition.c.id_kompetisi != id).where(Competition.c.deadline > datetime.datetime.now())
        # generate where not query
        for n in data:
            s2 = s2.where(Competition.c.id_kompetisi != n.id_kompetisi)

        res2 = connection.execute(s2)
        data2 = res2.fetchall()

        return {
            'data': data2
        }

def getDetail(id):
    query = select(select_column).select_from(join_sub_cat).where(Competition.c.id_kompetisi == id)
    result = connection.execute(query)

    response = {
        'data': result.fetchone(),
        'next': {},
        'prev': {}
    }

    # compoetition found
    print('result db', response)
    if( response['data'] != None):

        # update total views
        queryupdateviews = update(Competition).where(Competition.c.id_kompetisi == id).values(views = Competition.c.views + 1)
        connection.execute(queryupdateviews)

        # get next competition
        querynext = select([Competition.c.id_kompetisi.label('id'), Competition.c.judul_kompetisi.label('title')]).where(Competition.c.id_kompetisi > id).limit(1)
        resultnext = connection.execute(querynext).fetchone()
        if(resultnext): 
            response['next'] = {
                'id': encId(resultnext.id),
                'title': resultnext.title,
                'nospace_title': generateTitleUrl(resultnext.title)
            }


        # get prev competition
        queryprev = select([Competition.c.id_kompetisi.label('id'), Competition.c.judul_kompetisi.label('title')]).where(Competition.c.id_kompetisi < id).order_by(Competition.c.id_kompetisi.desc()).limit(1)
        resultprev = connection.execute(queryprev).fetchone()
        if(resultprev): 
            response['prev'] = {
                'id': encId(resultprev.id),
                'title': resultprev.title,
                'nospace_title': generateTitleUrl(resultprev.title)
            }

    return response