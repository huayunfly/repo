"""
Definition of urls helper functions
"""
from datetime import datetime
import timekit


def the_week_url():
    """
    Get the current week relative url
    @return: the week url
    """
    return '/timeline/%d/%02d/%d/' % \
           (datetime.now().year, datetime.now().month, timekit.monthweek(datetime.now()))
