from ..modules.db import connect
from users import Users
from sqlalchemy import Table, Column, MetaData, select, func, desc, BIGINT, INT, VARCHAR, DATETIME, Enum, TEXT

metadata = MetaData()

# table delaration
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
                    )

join_user = Competition.join(Users, Competition.c.id_user == Users.c.id_user)

select_column = [Competition.c.id_kompetisi]

def getList(Params = {}):
  s = select(select_column).order_by(Competition.c.id_kompetisi.desc()).select_from(join_user)
  c = select([func.count().label('total')]).select_from(join_user)

  # generate query
  if 'limit' in Params:
    s = s.limit(Params['limit'])
  if 'lastid' in Params:
    s = s.where(Competition.c.id < Params['lastid'])
  if 'tag' in Params:
    s = s.where(Competition.c.tag.like('%'+Params['tag']+'%'))
    c = c.where(Competition.c.tag.like('%'+Params['tag']+'%'))

  res = connect.execute(s)
  rescount = connect.execute(c)

  return {
    'data': res.fetchall(),
    'count': rescount.fetchone()['total']
  }
