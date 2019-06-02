from ..modules.db import connection
import datetime
import enum
from v2.helpers.encId import encId
from v2.helpers.strings import generateTitleUrl
from users import Users
from categories import MainCategory, SubCategory
from sqlalchemy import Table, Column, MetaData, select, update, func, Enum, BIGINT, INT, DATE, DATETIME, TEXT, or_, and_

metadata = MetaData()

# class FlagingEnum(enum.Enum):
#     1 = 1
#     0 = 0

# competition table declaration
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
                    Column('deadline', DATE),
                    Column('pengumuman', DATE),
                    Column('total_hadiah', INT),
                    Column('hadiah', TEXT),
                    Column('tag', TEXT),
                    Column('status', TEXT),
                    Column('rating', INT),
                    Column('views', INT),
                    Column('mediapartner', INT),
                    Column('garansi', TEXT),
                    Column('manage', TEXT),
                    Column('dataPengumuman', TEXT),
                    Column('dataGaleri', TEXT),
                    Column('kontak', TEXT),
                    Column('sumber', TEXT),
                    Column('ikuti', TEXT),
                    Column('id_main_kat', INT),
                    Column('id_sub_kat', INT),
                    )

CompetitionAction = Table("kompetisi_btn", metadata, 
    Column('id', BIGINT),
    Column('id_kompetisi', BIGINT),
    Column('id_user', BIGINT),
    Column('like', INT)
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
                 Competition.c.dataGaleri,
                 Competition.c.created_at, Competition.c.updated_at, Competition.c.deadline, Competition.c.pengumuman,
                 Competition.c.tag, Competition.c.hadiah, Competition.c.status, Competition.c.rating,
                 Competition.c.views,
                 Competition.c.mediapartner, Competition.c.garansi,
                 Competition.c.kontak, Competition.c.sumber,
                 Competition.c.id_user,
                 MainCategory.c.id_main_kat, MainCategory.c.main_kat,
                 SubCategory.c.id_sub_kat, SubCategory.c.sub_kat,
                 Users.c.username, Users.c.fullname, Users.c.moto, Users.c.level]

select_column_competition_action = [CompetitionAction.c.id, CompetitionAction.c.like]

# function to get list of competitions
def getList(Params={}):
    # order by
    orderby = Competition.c.id_kompetisi.desc()
    limit = 10
    if 'orderby' in Params:
        if Params['orderby'] == 'prize_dsc':
            orderby = Competition.c.total_hadiah.desc()

    if 'is_popular' in Params and Params['is_popular'] == True:
        orderby = Competition.c.views.desc()

    # generate query to get data
    s = select(select_column).select_from(join_sub_cat).order_by(orderby)

    # generate query to get count
    c = select([func.count().label('total')]).select_from(join_sub_cat)

    # limit result
    if 'limit' in Params:
        s = s.limit(Params['limit'])

    # filter result by id
    if 'lastid' in Params:
        if 'orderby' in Params:
            if Params['orderby'] == 'prize_dsc':
                s = s.where(Competition.c.total_hadiah < Params['lastprize'])
            else:
                s = s.where(Competition.c.id_kompetisi < Params['lastid'])
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
            s = s.where(and_(Competition.c.deadline > datetime.datetime.now(), Competition.c.status == "posted"))
            c = c.where(and_(Competition.c.deadline > datetime.datetime.now(), Competition.c.status == "posted"))
        elif Params['status'] == 'waiting':
            s = s.where(Competition.c.status == "waiting")
            c = c.where(Competition.c.status == "waiting")
        elif Params['status'] == 'reject':
            s = s.where(Competition.c.status == "reject")
            c = c.where(Competition.c.status == "reject")
        else :
            s = s.where(Competition.c.status == "posted")
            c = c.where(Competition.c.status == "posted")

    # show mediapartner
    if 'is_mediapartner' in Params and Params['is_mediapartner'] == True:
        s = s.where(Competition.c.mediapartner == 1)
        c = c.where(Competition.c.mediapartner == 1)

    # show guaranted competition
    if 'is_guaranted' in Params and Params['is_guaranted'] == True:
        s = s.where(Competition.c.garansi == "1")
        c = c.where(Competition.c.garansi == "1")

    # show popular competition
    if 'is_popular' in Params and Params['is_popular'] == True:
        s = s.where(or_(Competition.c.views > 50, Competition.c.views < 700))
        c = c.where(or_(Competition.c.views > 50, Competition.c.views < 700))

    # get competition by user_id
    if "user_id" in Params:
        s = s.where(Users.c.id_user == Params["user_id"])
        c = c.where(Users.c.id_user == Params["user_id"])

    res = connection.execute(s)
    rescount = connection.execute(c)

    return {
        'data': res.fetchall(),
        'count': rescount.fetchone()['total']
    }

# function to get competition related by competition id
def getRelated(id):
    # get detail competitoin
    c_query = select([Competition.c.id_main_kat.label('main_kat'), Competition.c.tag]).select_from(
        join_sub_cat).where(Competition.c.id_kompetisi == id)
    competition = connection.execute(c_query).fetchone()

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
        s2 = s2.where(Competition.c.id_kompetisi != id).where(
            Competition.c.deadline > datetime.datetime.now())
        # generate where not query
        for n in data:
            s2 = s2.where(Competition.c.id_kompetisi != n.id_kompetisi)

        res2 = connection.execute(s2)
        data2 = res2.fetchall()

        return {
            'data': data2
        }

# function to get detial competition by competition id
def getDetail(id):
    query = select(select_column).select_from(
        join_sub_cat).where(Competition.c.id_kompetisi == id)
    result = connection.execute(query)

    response = {
        'data': result.fetchone(),
        'next': {},
        'prev': {}
    }

    # compoetition found
    if(response['data'] != None):

        # update total views
        queryupdateviews = update(Competition).where(
            Competition.c.id_kompetisi == id).values(views=Competition.c.views + 1)
        connection.execute(queryupdateviews)

        # get next competition
        querynext = select([Competition.c.id_kompetisi.label('id'), Competition.c.judul_kompetisi.label(
            'title')]).where(Competition.c.id_kompetisi > id).limit(1)
        resultnext = connection.execute(querynext).fetchone()
        if(resultnext):
            response['next'] = {
                'id': encId(resultnext.id),
                'title': resultnext.title,
                'nospace_title': generateTitleUrl(resultnext.title)
            }

        # get prev competition
        queryprev = select([Competition.c.id_kompetisi.label('id'), Competition.c.judul_kompetisi.label(
            'title')]).where(Competition.c.id_kompetisi < id).order_by(Competition.c.id_kompetisi.desc()).limit(1)

        resultprev = connection.execute(queryprev).fetchone()
        if(resultprev):
            response['prev'] = {
                'id': encId(resultprev.id),
                'title': resultprev.title,
                'nospace_title': generateTitleUrl(resultprev.title)
            }

    return response

# function to get lattest competition
def getSingleLatest():
    query = select(select_column).select_from(join_sub_cat).order_by(
        Competition.c.id_kompetisi.desc()).limit(1)
    competition = connection.execute(query).fetchone()

    response = {
        'id': encId(competition.id_kompetisi),
        'title': competition.judul_kompetisi,
        'nospace_title': generateTitleUrl(competition.judul_kompetisi)
    }

    return response

# function to insert data into competition table
def insertData(params):
    query = Competition.insert().values(params)
    return connection.execute(query)

# function to update data competition by competition id
def updateData(params, id):
    query = Competition.update().where(Competition.c.id_kompetisi == id).values(params)
    return connection.execute(query)

# function to check is already like competition
def checkHaveLikedCompetition(params):

    print("check params", params)

    query = select(select_column_competition_action).select_from(
        CompetitionAction).where(and_(
            CompetitionAction.c.id_kompetisi == params["competition_id"],
            CompetitionAction.c.id_user == params["user_id"]
        ))
    resultAction = connection.execute(query).fetchone()

    # params for mysql query
    queryParams = {
        "id_kompetisi": params["competition_id"],
        "id_user": params["user_id"]
    }

    if resultAction :
        if("onlyCheck" in params) :
            # only check is checked
            return resultAction["like"] == 1
        else :
            # update data to unlike competition
            queryParams["like"] = 0 if resultAction["like"] == 1 else  resultAction["like"] == 0
            query = CompetitionAction.update().where(and_(
                CompetitionAction.c.id_kompetisi == params["competition_id"],
                CompetitionAction.c.id_user == params["user_id"]
            )).values(queryParams)
            connection.execute(query)
            return queryParams["like"] == 1
    else :
        if ("onlyCheck" in params) :
            # only check is cheked
            return False
        else :
            # insert new row
            queryParams["like"] = 1
            insertQuery = CompetitionAction.insert().values(queryParams)
            connection.execute(insertQuery)
            return True


# function to handle like/unlike competition