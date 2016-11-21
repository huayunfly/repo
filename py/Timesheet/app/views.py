"""
Definition of views.
"""
import calendar
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from datetime import datetime
from datetime import timedelta
from app.models import TaskTime
from app.models import Project
from app.models import Person

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
    task_mapping = {}
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
            if workday in task_mapping:
                # use workday as a key
                if task_mapping[workday] + task_percentage > 100:
                    # validation failed
                    has_error = True
                    break
            else:
                task_mapping[workday] = task_percentage
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
    """Renders the timeline page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        result = validate_task(request)
        if result[0]:
            return HttpResponseRedirect('/error/')
        else:
            # update the database
            for key, value in result[1].iteritems():
                day_project = key.split(DELIMITER)
                # day string format: 2016 Fri, Oct 21
                # retrieve year from 'year' parameter
                datetime0 = datetime.strptime('%s %s' % (year, day_project[0]), FORM_DATE_FORMAT)
                day = datetime(datetime0.year, datetime0.month, datetime0.day)
                project = Project.objects.get(project_id=day_project[1])
                percentage = value
                # Retrieving a single object with get()
                user = Person.objects.get(user=request.user)
                t_percentage = percentage / 100.0
                t_hours = float('%.1f' % (t_percentage * DAY_WORKING_HOURS))
                # INSERT or UPDATE a database row
                try:
                    tm = TaskTime.objects.get(workday=day, project=project)
                    tm.t_hours = t_hours
                    tm.t_percentage = t_percentage
                except TaskTime.DoesNotExist:
                    # add a new row in DB
                    tm = TaskTime(employee=user, t_hours=t_hours,
                                  t_percentage=t_percentage, workday=day, project=project)
                except TaskTime.MultipleObjectsReturned:
                    return HttpResponseRedirect('/error/')
                tm.save()
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

        tasks = TaskTime.objects.filter(employee__user__username=request.user.username,
                                                 workday__gte=weekdays[0],
                                                 workday__lte=weekdays[-1])

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
                'title': 'About',
                'message': 'Your timeline page',
                'year': datetime.now().year,
                'tasks': tasks,
                'projects': Project.objects.all(),
                'weekdays': weekdays,
                'projectID': create_names(task_num, PROJECT_ELEMENT_NAME, ELEMENT_ID_SURNAME),
                'dayID': create_names(task_num, DAY_ELEMENT_NAME, ELEMENT_ID_SURNAME),
                'timeID': create_names(task_num, TASKTIME_ELEMENT_NAME, ELEMENT_ID_SURNAME),
                'projectName': create_names(task_num, PROJECT_ELEMENT_NAME, ELEMENT_SURNAME),
                'dayName': create_names(task_num, DAY_ELEMENT_NAME, ELEMENT_SURNAME),
                'timeName': create_names(task_num, TASKTIME_ELEMENT_NAME, ELEMENT_SURNAME),
                'emptyTasks': range(empty_task_num),
            }
        )
