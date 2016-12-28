# -*- coding: utf-8 -*-
"""
@summary: Definition of views.
@author: Yun Hua, yun_hua@yashentech.com
@date: 2016.12.06
"""
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from datetime import datetime
from datetime import timedelta
from .models import TaskTime
from .models import Project
from .models import Person
from .models import NoWorkingDay
from .models import FrozenDateRange
import utils.timekit
from utils.urls import the_week_url
from utils.unicodecsv import UnicodeWriter

WEEK_DAYS_NUM = 7
DAY_WORKING_HOURS = 8.0

# Basename for creating unique name and id for the html-table cell.
PROJECT_ELEMENT_NAME = 'projectSel'
DAY_ELEMENT_NAME = 'daySel'
TASKTIME_ELEMENT_NAME = 'percentageInput'
ELEMENT_SURNAME = 'form'
ELEMENT_ID_SURNAME = 'id_form'
TASKTIME_SUFFIX = '%'
PLACEHOLD_TASKTIME_NUM = 5

FORM_DATE_FORMAT = '%Y %a, %b %d'
WEEK_LINK_FORMAT = '/timeline/%d/%02d/%d/'
REPORT_DATE_FORMAT = '%Y-%m-%d'
OUTPUT_DATE_FORMAT = '%d-%02d-%02d'
DELIMITER = '_'

REPORT_Q_PROJECT = 'project_id'
REPORT_Q_DATE_BEGIN = 'date__gte'
REPORT_Q_DATE_END = 'date__lt'
REPORT_Q_FORMAT = 'output_type'

REPORT_CSV_TYPE = 'csv'


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


def start(request):
    """Renders the start page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return HttpResponseRedirect(the_week_url())
    else:
        return HttpResponseRedirect('/')


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
            'title': '工时表 (0.1)',
            'message': '亚申科技',
            'mail': 'yun_hua@yashentech.com',
            'year': datetime.now().year,
        }
    )


def thanks(request):
    """Renders the thanks page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/thanks.html',
        {
            'title': 'Thanks',
            'message': 'Operate successfully',
            'year': datetime.now().year,
        }
    )


def error(request):
    """Renders the error page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/error.html',
        {
            'title': 'Error',
            'message': 'Operation failed',
            'year': datetime.now().year,
        }
    )


def validate_task(request):
    """Validate the timeline form data. The sum of task time in a day cannot be exceed 100(%).
        Empty task time equal 0(%) will ignored.
        It also merges the same project task entries in the same day.
        For example: Mon, Jan 1 - T899 - 10(%); Mon, Jan - T899 - 20(%); = Mon, Jan - T899 - 30(%)
        for example: pub_date html input field, name=form-1-pub_date, id=id_form-1-pub_date
        @param request: HttpRequest object
        @return (has_error<BOOL>, data<dict>): tuple including validate result and table data mappings.
    """
    has_error = False
    i = 0
    day_task_mapping = {}
    project_mapping = {}
    while i >= 0:
        key = create_name(i, DAY_ELEMENT_NAME, ELEMENT_SURNAME)
        workday = request.POST.get(key)
        if workday is None:
            # POST iteration complete
            break
        else:
            key = create_name(i, PROJECT_ELEMENT_NAME, ELEMENT_SURNAME)
            proj = request.POST.get(key)
            key = create_name(i, TASKTIME_ELEMENT_NAME, ELEMENT_SURNAME)
            task_percentage = request.POST.get(key)
            if (proj is None) or (task_percentage is None):
                # validation failed
                has_error = True
                break
            try:
                task_percentage = int(task_percentage.rstrip(TASKTIME_SUFFIX))
            except ValueError:
                # validation failed
                has_error = True
                break
            if task_percentage < 0 or task_percentage > 100:
                # validation failed
                has_error = True
                break
            if 0 == task_percentage:
                # drop the empty task time
                i += 1
                continue
            if workday in day_task_mapping:
                # use workday as a key
                if day_task_mapping[workday] + task_percentage > 100:
                    # validation failed
                    has_error = True
                    break
                else:
                    day_task_mapping[workday] += task_percentage
            else:
                day_task_mapping[workday] = task_percentage
            # create a key to merge the same project task in a single day
            taskkey = workday + DELIMITER + proj
            if taskkey in project_mapping:
                project_mapping[taskkey] += task_percentage
            else:
                project_mapping[taskkey] = task_percentage
            i += 1
    return [has_error, project_mapping]


def create_names(number, element_name, surname):
    """Create unique names for the form elements
     for example: 'pub_date' form input element, element_name=pub_date, surname=form,
     then the format will be form-0-pub_date, form-1-pub_date
    @param number: the total number of elements, which is used to make name unique
    @param element_name: the form element base name
    @param surname: the form element's base name
    @return the name list
    """
    return ['%s-%d-%s' % (surname, n, element_name) for n in range(number)]


def create_name(index, element_name, surname):
    """Create a name for the form element
     for example: 'pub_date' form input element, element_name=pub_date, surname=form,
     then the format will be form-index-pub_date
    @param index: an integer
    @param element_name: the form element base name
    @param surname: the form element's base name
    @return the name
    """
    return '%s-%d-%s' % (surname, index, element_name)


def timeline(request, year, month, week=0):
    """Renders the timeline page.
    @param request: a HttpRequest
    @param year: year
    @param month: month
    @param week: the week number of a month
    """
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    monday = utils.timekit.getmonday(int(year), int(month), int(week))
    sunday = monday + timedelta(days=WEEK_DAYS_NUM - 1)

    if request.method == 'POST':
        if FrozenDateRange.objects.count() > 0:
            frozen_date_lt = FrozenDateRange.objects.first().update_lt
            delta = frozen_date_lt - sunday
            if delta.days > 0:
                return HttpResponseRedirect('/error/')

        result = validate_task(request)
        if result[0]:
            return HttpResponseRedirect('/error/')
        else:
            # Query in the week.
            week_tasks = TaskTime.objects.filter(employee__user__username=request.user.username,
                                                 workday__lte=sunday, workday__gte=monday)
            # Synchronize the form data and the database.
            for key, value in result[1].iteritems():
                day_project = key.split(DELIMITER)
                # day string format: 2016 Fri, Oct 21
                # retrieve year from 'year' parameter
                datetime0 = datetime.strptime('%s %s' % (year, day_project[0]), FORM_DATE_FORMAT)
                day = datetime(datetime0.year, datetime0.month, datetime0.day)
                project = Project.objects.get(project_id=day_project[1])
                percentage = value
                # Retrieving a single object with get().
                user = Person.objects.get(user=request.user)
                t_percentage = percentage / 100.0
                t_hours = float('%.1f' % (t_percentage * DAY_WORKING_HOURS))
                # INSERT or UPDATE a database row, the updated one wil be excluded from Query.
                try:
                    tm = week_tasks.get(workday=day, project=project)
                    tm.t_hours = t_hours
                    tm.t_percentage = t_percentage
                except TaskTime.DoesNotExist:
                    # add a new row in DB
                    tm = TaskTime(employee=user, t_hours=t_hours,
                                  t_percentage=t_percentage, workday=day, project=project)
                except TaskTime.MultipleObjectsReturned:
                    return HttpResponseRedirect('/error/')
                tm.save()
                week_tasks = week_tasks.exclude(workday=day, project=project)
            # Delete the row not in the user form.
            week_tasks.delete()
            return HttpResponseRedirect('/thanks/')
    else:
        weekdays = []
        no_working_q = NoWorkingDay.objects.filter(date__lte=sunday,
                                                   date__gte=monday)
        no_working_days = [item.date for item in no_working_q]
        for day in range(0, WEEK_DAYS_NUM, 1):
            nextday = monday + timedelta(days=day)
            if nextday not in no_working_days:
                weekdays.append(nextday)

        tasks = TaskTime.objects.filter(employee__user__username=request.user.username,
                                        workday__gte=weekdays[0],
                                        workday__lte=weekdays[-1]).order_by('workday')

        # For week links
        nextweek = utils.timekit.nextweek(int(year), int(month), int(week))
        lastweek = utils.timekit.lastweek(int(year), int(month), int(week))
        theweek = utils.timekit.currentweek()

        # For output query
        month_start = OUTPUT_DATE_FORMAT % (int(year), int(month), 1)
        if int(month) + 1 > 12:
            next_month_start = OUTPUT_DATE_FORMAT % (int(year) + 1, 1, 1)
        else:
            next_month_start = OUTPUT_DATE_FORMAT % (int(year), int(month) + 1, 1)

        # If there is no task, then we create empty tasks in the browser.
        task_num = len(tasks)
        empty_task_num = PLACEHOLD_TASKTIME_NUM
        if 0 == task_num:
            task_num = PLACEHOLD_TASKTIME_NUM
        else:
            empty_task_num = 0

        return render(
            request,
            'app/timeline.html',
            {
                'queryMonth': int(month),
                'queryYear': int(year),
                'queryWeek': int(week),
                'nextLink': WEEK_LINK_FORMAT % (nextweek[0], nextweek[1], nextweek[2]),
                'prevLink': WEEK_LINK_FORMAT % (lastweek[0], lastweek[1], lastweek[2]),
                'currentLink': WEEK_LINK_FORMAT % (theweek[0], theweek[1], theweek[2]),
                'message': 'Hello',
                'year': datetime.now().year,
                'tasks': tasks,
                'projects': Project.objects.all().order_by('project_id'),
                'weekdays': weekdays,
                'projectID': create_names(task_num, PROJECT_ELEMENT_NAME, ELEMENT_ID_SURNAME),
                'dayID': create_names(task_num, DAY_ELEMENT_NAME, ELEMENT_ID_SURNAME),
                'timeID': create_names(task_num, TASKTIME_ELEMENT_NAME, ELEMENT_ID_SURNAME),
                'projectName': create_names(task_num, PROJECT_ELEMENT_NAME, ELEMENT_SURNAME),
                'dayName': create_names(task_num, DAY_ELEMENT_NAME, ELEMENT_SURNAME),
                'timeName': create_names(task_num, TASKTIME_ELEMENT_NAME, ELEMENT_SURNAME),
                'emptyTasks': range(empty_task_num),
                'month_start': month_start,
                'next_month_start': next_month_start,
            }
        )


def report(request):
    """Generate the report."""
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        pass
    elif request.is_ajax():
        # Do NOT use urlparse(request.get_raw_uri()).query here, which causes bad encoding/decoding problem
        project_id = request.GET.get(REPORT_Q_PROJECT)
        date_begin = request.GET.get(REPORT_Q_DATE_BEGIN)
        date_end = request.GET.get(REPORT_Q_DATE_END)
        if (project_id is not None) and (date_begin is not None) and (date_end is not None):
            tasks = TaskTime.objects.filter(project__project_id=project_id,
                                            workday__gte=date_begin,
                                            workday__lt=date_end)
        # In order to allow non-dict objects to be serialized set the safe parameter to False.
        return JsonResponse({'data': [(task.employee.display_name,
                                       task.workday.strftime(REPORT_DATE_FORMAT), task.t_hours) for task in tasks]})

    else:
        today = datetime.today()
        month_start = datetime(today.year, today.month, 1)
        if today.month + 1 > 12:
            next_month_start = datetime(today.year + 1, 1, 1)
        else:
            next_month_start = datetime(today.year, today.month + 1, 1)

        if today.month - 1 < 1:
            last_month_start = datetime(today.year - 1, 12, 1)
        else:
            last_month_start = datetime(today.year, today.month - 1, 1)
        year_start = datetime(today.year, 1, 1)
        next_year_start = datetime(today.year + 1, 1, 1)

        project_id = request.GET.get(REPORT_Q_PROJECT)
        date_begin = request.GET.get(REPORT_Q_DATE_BEGIN)
        date_end = request.GET.get(REPORT_Q_DATE_END)
        if (project_id is not None) and (date_begin is not None) and (date_end is not None):
            tasks = TaskTime.objects.filter(project__project_id=project_id,
                                            workday__gte=date_begin,
                                            workday__lt=date_end)
        else:
            tasks = None

        return render(
            request,
            'app/report.html',
            {
                'title': 'Report',
                'message': 'Project related',
                'year': datetime.now().year,
                'projects': Project.objects.all().order_by('project_id'),
                'month_start': month_start.strftime(REPORT_DATE_FORMAT),
                'last_month_start': last_month_start.strftime(REPORT_DATE_FORMAT),
                'next_month_start': next_month_start.strftime(REPORT_DATE_FORMAT),
                'year_start': year_start.strftime(REPORT_DATE_FORMAT),
                'next_year_start': next_year_start.strftime(REPORT_DATE_FORMAT),
                'tasks': tasks,
            }
        )


def output(request):
    """Generate the output."""
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'GET':
        date_begin = request.GET.get(REPORT_Q_DATE_BEGIN)
        date_end = request.GET.get(REPORT_Q_DATE_END)
        fmt = request.GET.get(REPORT_Q_FORMAT)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename="%s_%s.csv"' % (request.user.username, date_begin)

        tasks = []
        if (date_begin is not None) and (date_end is not None) and (fmt is not None):
            if fmt == REPORT_CSV_TYPE:
                date_begin = datetime.strptime(date_begin, REPORT_DATE_FORMAT)
                date_end = datetime.strptime(date_end, REPORT_DATE_FORMAT)
                tasks = TaskTime.objects.filter(employee__user=request.user,
                                                workday__gte=date_begin,
                                                workday__lt=date_end).order_by('workday')

        if request.user.person:
            writer = UnicodeWriter(response)
            line = ['', '', '', '']
            for task in tasks:
                line[0] = request.user.person.display_name
                line[1] = task.workday.strftime(REPORT_DATE_FORMAT)
                line[2] = task.project.project_id
                line[3] = '%0.2f' % task.t_percentage
                writer.writerow(line)

        return response
    else:
        return HttpResponseRedirect('/')
