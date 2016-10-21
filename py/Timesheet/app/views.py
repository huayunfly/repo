"""
Definition of views.
"""
import calendar
import time
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from datetime import timedelta
from app.models import TaskTime
from app.models import Project
from app.models import Person
from .forms import TimelineForm

WEEK_DAYS_NUM = 7
DAY_WORKING_HOURS = 8.0
# constants for creating unique name and id for the html-table cell. e.g. 0.projectSel, 1.daySel
PROJECT_CELL_ID = '-projectSel'
DAY_CELL_ID = '-daySel'
TASKTIME_CELL_ID = '-percentageInput'
DELIMITER = '_'


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


def validate_task(request):
    """Validate the timeline form data
        for example: pub_date html input field, name=form-1-pub_date, id=id_form-1-pub_date
        @param request: HttpRequest object
        @return (has_error<BOOL>, data<dict>): tuple including validate result and table data mappings.
    """
    has_error = False
    i = 0
    mappings = {}
    while i >= 0:
        workday = request.POST.get(str(i) + DAY_CELL_ID)
        if workday is None:
            # POST iteration complete
            break
        else:
            proj = request.POST.get(str(i) + PROJECT_CELL_ID)
            hours = request.POST.get(str(i) + TASKTIME_CELL_ID)
            if (proj is None) or (hours is None):
                # validation failed
                has_error = True
                break
            try:
                hours = float(hours)
            except ValueError:
                # validation failed
                has_error = True
                break
            if hours < 0.0:
                # validation failed
                has_error = True
                break
            # create a key
            taskkey = workday + DELIMITER + proj
            if taskkey in mappings:
                if mappings[taskkey] + hours > 1.0:
                    # validation failed
                    has_error = True
                    break
                else:
                    # merge the task hours under the same day and project
                    mappings[taskkey] += hours
            else:
                mappings[taskkey] = hours
            i += 1
    return [has_error, mappings]


def timeline(request, year, month, week=0):
    """Renders the timeline page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        result = validate_task(request)
        if result[0]:
            return HttpResponseRedirect('/error/')
        else:
            # update the database
            for item in result[1].iteritems():
                day_project = item[0].split(DELIMITER)
                # day string format: 2016 Fri, Oct 21
                daystring = datetime.strptime('%s %s' % (year, day_project[0]), '%Y %a, %b %d')
                day = datetime(daystring.year, daystring.month, daystring.day)
                project = Project.objects.get(project_id=day_project[1])
                percentage = item[1]
                user = Person.objects.get(user=request.user)
                t1 = TaskTime(employee=user, t_hours=percentage * DAY_WORKING_HOURS,
                              t_percentage=percentage, workday=day, project=project)
                t1.save()

            return HttpResponseRedirect('/thanks/')
    else:
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

        form = TimelineForm()

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
                'form': form,
                'projectID': PROJECT_CELL_ID,
                'dayID': DAY_CELL_ID,
                'timeID': TASKTIME_CELL_ID,
            }
        )
