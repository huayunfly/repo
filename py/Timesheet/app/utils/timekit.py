"""
Definition of datetime helper functions.
"""

from datetime import datetime
from datetime import timedelta
import calendar

WEEK_DAYS_NUM = 7

def monthweek(date):
    """Get the week of the month to which a day belongs
    @param date: a day
    @return: the week number from 1
    """
    whatday = date.isoweekday()
    lastsunday = date.day - whatday
    if lastsunday <= 0:
        return 1
    weeks = lastsunday / 7
    if (lastsunday % 7) > 0:
        return weeks + 1 + 1
    else:
        return weeks + 1


def lastweek(year, month, week):
    """
    Get the last week tuple.
    @param year: the year number, 2016 e.g.
    @param month: the month number, 12 e.g.
    @param week: the week number, start from 1
    @return: last week tuple (year, month, week)
    """
    lastmonday = getmonday(year, month, week) - timedelta(days=WEEK_DAYS_NUM)
    return lastmonday.year, lastmonday.month, monthweek(lastmonday)


def nextweek(year, month, week):
    """
    Get the next week tuple.
    @param year: the year number, 2016 e.g.
    @param month: the month number, 12 e.g.
    @param week: the week number, start from 1
    @return: next week tuple (year, month, week)
    """
    nextmonday = getmonday(year, month, week) + timedelta(days=WEEK_DAYS_NUM)
    return nextmonday.year, nextmonday.month, monthweek(nextmonday)


def currentweek():
    """
    Get the current week tuple.
    @return: current week tuple (year, month, week)
    """
    today = datetime.now()
    return today.year, today.month, monthweek(today)


def getmonday(year, month, week):
    """
    Get Monday according to the week number.
    @param year: the year number, 2016 e.g.
    @param month: the month number, 12 e.g.
    @param week: the week number, start from 1. If week equals 0,
                    it will redirect to the last week.
    @return: Monday in datetime
    """
    weeks = calendar.monthcalendar(year, month)
    if 0 == week or week > len(weeks):
        week = -1
    else:
        week -= 1
    # Find the first day in one week of this month like [0, 0, 0, 0, 1, 2, 3]
    first = 0
    for day in range(0, WEEK_DAYS_NUM, 1):
        if 0 != weeks[week][day]:
            first = day
            break
    return datetime(int(year), int(month), weeks[week][first]) - timedelta(days=first)







