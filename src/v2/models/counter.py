from ..modules.db import connection
from competitions import Competition
from news import News
from competitions import Competition
from ..modules.db import connection
from ..modules.number import convertToRelativeCurrency
from sqlalchemy import select, func, and_
import datetime
import calendar
from decimal import Decimal

selectCountCompetition = [Competition.c.id_kompetisi]


def homeCounter():
    # ref: https://stackoverflow.com/a/30071999/2780875
    now = datetime.datetime.now()

    # get count of competitio
    queryCount = select([func.count().label('total')]).select_from(Competition)
    querySumPrize = select([func.sum(Competition.c.total_hadiah).label('total')]).select_from(Competition)

    # generate mindate and maxdate of this month
    # ref: https://stackoverflow.com/a/11619039/2780875
    currentYear = now.year
    currentMonth = now.month

    totalDays = calendar.monthrange(currentYear, currentMonth)[1]
    startDate = datetime.date(currentYear, currentMonth, 1)
    endDate = datetime.date(currentYear, currentMonth, totalDays)

    queryCountActiveCompetition = queryCount.where(Competition.c.deadline > datetime.datetime.now())
    queryCountActiveCompetitionThisMount = queryCount.where(and_(Competition.c.deadline >= startDate, Competition.c.deadline <= endDate))
    querySumPrizeActive= querySumPrize.where(Competition.c.deadline > datetime.datetime.now())
    
    resCountActiveCompetition = connection.execute(queryCountActiveCompetition)
    resCountActiveCompetitionThisMount = connection.execute(queryCountActiveCompetitionThisMount)
    resSumPrize = connection.execute(querySumPrizeActive)

    return {
        "activeCompetition": resCountActiveCompetition.fetchone()['total'],
        "deadlineThisMonth": resCountActiveCompetitionThisMount.fetchone()['total'],
        # ref: https://groups.google.com/forum/#!topic/sqlalchemy/3fipkThttQA
        "totalPrizeActiveCompetition": convertToRelativeCurrency(int(resSumPrize.fetchone()['total'])),
    }


def superSidebarCounter():
    return {

    }
