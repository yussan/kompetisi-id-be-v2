from ..modules.db import connection
from sqlalchemy import Table, Column, MetaData, BIGINT, TEXT, select
from competitions import Competition, join_sub_cat, select_column as select_column_competition, func

metadata = MetaData()

CompetitionSubscription = Table('kompetisi_langganan', metadata,
  Column("id_kompetisi_langganan", BIGINT),
  Column("id_kompetisi", BIGINT),
  Column("id_user", BIGINT)
)

join_competition_subscription = join_sub_cat.join(CompetitionSubscription, Competition.c.id_kompetisi == CompetitionSubscription.c.id_kompetisi)

check_status_column = [CompetitionSubscription.c.id_kompetisi_langganan]

# function to get status subscription based on user_id and competition_id
def checkHaveSubscribedCompetition(Params):
  s = select(check_status_column) \
    .select_from(CompetitionSubscription) \
    .where(CompetitionSubscription.c.id_user == Params['user_id']) \
    .where(CompetitionSubscription.c.id_kompetisi == Params['competition_id'])

  res = connection.execute(s)
  data = res.fetchall()

  return len(data) > 0

# function to get list subscribed competition by user_id
# list from competition list
def subscribeList(Params):

  orderby = Competition.c.id_kompetisi.desc()
  limit = Params['limit'] if 'limit' in Params else 10

  s = select(select_column_competition)\
    .select_from(join_competition_subscription)\
      .where(CompetitionSubscription.c.id_user == Params["user_id"])\
        .order_by(orderby)\
          .limit(limit)
  c = select([func.count().label('total')])\
    .select_from(join_competition_subscription)\
      .where(CompetitionSubscription.c.id_user == Params["user_id"])

  if 'lastid' in Params:
    s = s.where(Competition.c.id_kompetisi < Params['lastid'])

  res = connection.execute(s)
  rescount = connection.execute(c)

  return {
      'data': res.fetchall(),
      'count': rescount.fetchone()['total']
  }

# function subscribe action (subscribe / unsubscribe)
def subscribeAction(Params):
  # check is already subscribed or not
  is_subscribed = checkHaveSubscribedCompetition(Params) 

  print("is sibscribed", is_subscribed, Params)

  if is_subscribed :
    # delete from table kompetisi_langganan
    query = CompetitionSubscription.delete()\
      .where(CompetitionSubscription.c.id_user == Params['user_id'])\
        .where(CompetitionSubscription.c.id_kompetisi == Params['competition_id'])
  else:
    # insert into table
    query = CompetitionSubscription.insert()\
      .values({
        'id_kompetisi': Params['competition_id'],
        'id_user': Params['user_id']
      })

  return connection.execute(query)