"""
Definition of views.
"""
import calendar
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from datetime import timedelta
from app.models import TaskTime
from app.models import Project
from app.models import Person

WEEK_DAYS_NUM = 7


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )


def timeline(request, year, month, week=0):
    """Renders the timeline page."""
    assert isinstance(request, HttpRequest)
    weeks = calendar.monthcalendar(int(year), int(month))
    weeknumber = int(week)
    if 0 == weeknumber or weeknumber > len(weeks):
        weeknumber = -1
    else:
        weeknumber -= 1

    # Find the first day in one week of this month like [0, 0, 0, 0, 1, 2, 3]
    first = 0
    for day in range(0, WEEK_DAYS_NUM, 1):
        if 0 != weeks[weeknumber][day]:
            first = day
            break

    # Make a valid week range which may cover the last month or the next month.
    monday = datetime(int(year), int(month), weeks[weeknumber][first]) - timedelta(days=first)
    weekdays = [monday]
    for day in range(1, WEEK_DAYS_NUM, 1):
        weekdays.append(monday + timedelta(days=day))

    return render(
        request,
        'app/timeline.html',
        {
            'title': 'About',
            'message': 'Your timeline page',
            'year': datetime.now().year,
            'tasks': TaskTime.objects.filter(employee__user__username=request.user.username,
                                             workday__gte=weekdays[0],
                                             workday__lte=weekdays[-1]),
            'projects': Project.objects.all(),
            'weekdays': weekdays,
        }
    )
