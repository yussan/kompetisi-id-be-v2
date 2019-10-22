from ..modules.db import connection
from ..modules.db import connection
from ..modules.number import convertToRelativeCurrency
from competitions import Competition, join_sub_cat
from news import News
from request import Request
from competitions import Competition
from competitions_subscription import CompetitionSubscription
from users import Users
from news import News, join_user
from sqlalchemy import select, func, and_, or_
import datetime
import calendar
from decimal import Decimal


def homeCounter():
    # ref: https://stackoverflow.com/a/30071999/2780875
    now = datetime.datetime.now()

    # get count of competition
    queryCount = select([func.count().label('total')]).select_from(Competition)
    querySumPrize = select(
        [func.sum(Competition.c.total_hadiah).label('total')]).select_from(Competition)

    # generate mindate and maxdate of this month
    # ref: https://stackoverflow.com/a/11619039/2780875
    currentYear = now.year
    currentMonth = now.month

    totalDays = calendar.monthrange(currentYear, currentMonth)[1]
    startDate = datetime.date(currentYear, currentMonth, 1)
    endDate = datetime.date(currentYear, currentMonth, totalDays)

    queryCountActiveCompetition = queryCount.where(
        Competition.c.deadline > datetime.datetime.now())
    queryCountActiveCompetitionThisMount = queryCount.where(
        and_(Competition.c.deadline >= startDate, Competition.c.deadline <= endDate))
    querySumPrizeActive = querySumPrize.where(
        Competition.c.deadline > datetime.datetime.now())

    # execute query

    resCountActiveCompetition = connection.execute(queryCountActiveCompetition)
    resCountActiveCompetitionThisMount = connection.execute(
        queryCountActiveCompetitionThisMount)
    resSumPrize = connection.execute(querySumPrizeActive)

    return {
        "activeCompetition": resCountActiveCompetition.fetchone()['total'],
        "deadlineThisMonth": resCountActiveCompetitionThisMount.fetchone()['total'],
        # ref: https://groups.google.com/forum/#!topic/sqlalchemy/3fipkThttQA
        "totalPrizeActiveCompetition": convertToRelativeCurrency(int(resSumPrize.fetchone()["total"]))
    }


def superSidebarCounter():

    # get count competition
    qCountC = select([func.count().label('total')]).select_from(
        join_sub_cat)

    # get count competition by condition
    qLiveC = qCountC.where(and_(Competition.c.deadline >
                                datetime.datetime.now(), Competition.c.status == "posted"))
    qWaitingC = qCountC.where(Competition.c.status == "waiting")
    qPostedC = qCountC.where(Competition.c.status == "posted")
    qDraftC = qCountC.where(Competition.c.status == "draft")
    qRejectC = qCountC.where(Competition.c.status == "reject")

    # get count news
    qCountN = select([func.count().label("total")]).select_from(join_user)

    # get count news by condition
    qPostedN = qCountN.where(News.c.draft != "1")
    qDraftN = qCountN.where(News.c.draft == "1")

    # get count request
    qCountR = select([func.count().label('total')]).select_from(
        Request)

    # get count request by condition
    qTotalR = qCountR
    qWaitingR = qCountR.where(Request.c.status == "waiting")
    qAcceptR = qCountR.where(Request.c.status == "posted")
    qRejectR = qCountR.where(Request.c.status == "reject")

    # get count users
    qCountU = select([func.count().label('total')]).select_from(
        Users)

    # get count user by condition
    qVerifiedU = qCountU.where( and_(Users.c.status == "active", Users.c.is_verified == 1))
    qUnverifiedU = qCountU.where( and_(Users.c.status == "active")).where( or_(Users.c.is_verified != 1, Users.c.is_verified == None))
    qBannedU = qCountU.where(Users.c.status == "banned")

    # execute query
    rLiveC = connection.execute(qLiveC)
    rWaitingC = connection.execute(qWaitingC)
    rPostedC = connection.execute(qPostedC)
    rDraftC = connection.execute(qDraftC)
    rRejectC = connection.execute(qRejectC)

    rPostedN = connection.execute(qPostedN)
    rDraftN = connection.execute(qDraftN)

    rTotalR = connection.execute(qTotalR)
    rWaitingR = connection.execute(qWaitingR)
    rAcceptR = connection.execute(qAcceptR)
    rRejectR = connection.execute(qRejectR)

    rVerifiedU = connection.execute(qVerifiedU)
    rUnverifiedU = connection.execute(qUnverifiedU)
    rBannedU = connection.execute(qBannedU)

    return {
        "competition": {
            "live": rLiveC.fetchone()["total"],
            "waiting": rWaitingC.fetchone()["total"],
            "posted": rPostedC.fetchone()["total"],
            "draft": rDraftC.fetchone()["total"],
            "reject": rRejectC.fetchone()["total"],
            "draft": 0,
        },
        "request": {
            "total": rTotalR.fetchone()["total"],
            "waiting": rWaitingR.fetchone()["total"],
            "accept": rAcceptR.fetchone()["total"],
            "reject": rRejectR.fetchone()["total"],
        },
        "news": {
            "posted": rPostedN.fetchone()["total"],
            "draft": rDraftN.fetchone()["total"],
        },
        "members": {
            "verified": rVerifiedU.fetchone()["total"],
            "unverified": rUnverifiedU.fetchone()["total"],
            "banned": rBannedU.fetchone()["total"]
        }
    }


def dashboardSidebarCounter(user_id):
    # get count competition
    join_user = Competition.join(
        Users, Competition.c.id_user == Users.c.id_user)
    qCountC = select([func.count().label('total')]).select_from(
        join_user)

    # query
    qWaitingC = qCountC.where(
        and_(Competition.c.status == "waiting", Users.c.id_user == user_id))
    qRejectC = qCountC.where(
        and_(Competition.c.status == "reject", Users.c.id_user == user_id))
    qPostedC = qCountC.where(
        and_(Competition.c.status == "posted", Users.c.id_user == user_id))
    qLiveC = qCountC.where(and_(Competition.c.status == "posted", Users.c.id_user ==
                                user_id, Competition.c.deadline > datetime.datetime.now()))
    # qSubscribedC = select([func.count().label('total')])\
    #     .select_from(CompetitionSubscription)\
    #         .where(CompetitionSubscription.c.id_user == user_id)

    # execute query
    rWaitingC = connection.execute(qWaitingC)
    rPostedC = connection.execute(qPostedC)
    rRejectC = connection.execute(qRejectC)
    rLiveC = connection.execute(qLiveC)
    # rSubscribedC = connection.execute(qSubscribedC)

    return {
        "competition": {
            "waiting": rWaitingC.fetchone()["total"],
            "posted": rPostedC.fetchone()["total"],
            "rejected": rRejectC.fetchone()["total"],
            "live": rLiveC.fetchone()["total"],
            "subscribed": 0,
            "liked": 0,
        }
    }
