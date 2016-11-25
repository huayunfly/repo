"""
Definition of datetime helper functions.
"""

from datetime import datetime
import calendar

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
