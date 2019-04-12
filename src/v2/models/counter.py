from ..modules.db import connection
from competitions import Competition
from news import News


def homeCounter():
    return {
        "activeCompetition": 0,
        "deadlineThisMonth": 0,
        "totalPrizeThisMonth": 0,
    }


def superSidebarCounter():
    return {

    }
