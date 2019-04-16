from ..modules.db import connection
from competitions import Competition
from news import News
from request import Request
from competitions import Competition
from news import News
from users import Users
from ..modules.db import connection
from ..modules.number import convertToRelativeCurrency
from sqlalchemy import select, func, and_
import datetime
import calendar
from decimal import Decimal

def homeCounter():
    # ref: https://stackoverflow.com/a/30071999/2780875
    now = datetime.datetime.now()

    # get count of competitio
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
        "totalPrizeActiveCompetition": convertToRelativeCurrency(int(resSumPrize.fetchone()['total'])),
    }


def superSidebarCounter():

    # get count competition
    qCountC = select([func.count().label('total')]).select_from(
        Competition)

    # get count competition by condition
    qLiveC = qCountC.where(Competition.c.deadline > datetime.datetime.now())
    qWaitingC = qCountC.where(Competition.c.status == "waiting")
    qPostedC = qCountC.where(Competition.c.status == "posted")
    qDraftC = qCountC.where(Competition.c.status == "draft")
    qRejectC = qCountC.where(Competition.c.status == "reject")

    # get count news
    qCountN = select([func.count().label("total")]).select_from(News)

    # get count news by condition
    qPostedN = qCountN.where(News.c.status == "post")
    qDraftN = qCountN.where(News.c.status == "draft")

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
    qActiveU = qCountU.where(Users.c.status == "active")
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

    rActiveU = connection.execute(qActiveU)
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
            "active": rActiveU.fetchone()["total"],
            "banned": rBannedU.fetchone()["total"]
        }
    }
