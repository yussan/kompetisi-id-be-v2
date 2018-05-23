from ..modules.db import connect
from users import Users
from sqlalchemy import Table, Column, MetaData, select, func, desc, BIGINT, INT, VARCHAR, DATETIME, Enum, TEXT

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

select_column = [Competition.c.id_kompetisi, Competition.c.judul_kompetisi, Competition.c.sort, Competition.c.poster, Competition.c.penyelenggara,
                 Competition.c.hadiah, Competition.c.total_hadiah, 
                 Competition.c.konten, Competition.c.sumber, Competition.c.ikuti, 
                 Competition.c.dataPengumuman,
                 Competition.c.created_at, Competition.c.updated_at, Competition.c.deadline, Competition.c.pengumuman,
                 Competition.c.tag, Competition.c.hadiah, Competition.c.status, Competition.c.rating, Competition.c.views, 
                 Competition.c.mediapartner, Competition.c.garansi, 
                 Competition.c.kontak, Competition.c.sumber,
                 MainCategory.c.id_main_kat, MainCategory.c.main_kat,
                 SubCategory.c.id_sub_kat, SubCategory.c.sub_kat,
                 Users.c.username, Users.c.fullname]


def getList(Params={}):
    # generate query to get data
    s = select(select_column).order_by(Competition.c.id_kompetisi.desc()).select_from(join_sub_cat)

    # generate query to get count
    c=select([func.count().label('total')]).select_from(Competition)

    # generate query
    if 'limit' in Params:
        s=s.limit(Params['limit'])
    if 'lastid' in Params:
        s=s.where(Competition.c.id < Params['lastid'])
    if 'tag' in Params:
        s=s.where(Competition.c.tag.like('%'+Params['tag']+'%'))
        c=c.where(Competition.c.tag.like('%'+Params['tag']+'%'))

    res=connect.execute(s)
    rescount=connect.execute(c)

    return {
        'data': res.fetchall(),
        'count': rescount.fetchone()['total']
    }
