# _*_ coding: utf-8 _*_
# !/usr/bin/env python
"""
Command-line utility for administrative tasks.
"""

import os
from datetime import datetime
import django
from xml.dom.minidom import parse

if __name__ == "__main__":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "Timesheet.settings"
    )

    # Removes all data from the database
    from django.core.management import execute_from_command_line

    execute_from_command_line(['', 'flush'])

    # Avoid error while importing User: django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
    django.setup()

    from django.contrib.auth.models import User
    from django.contrib.auth.hashers import make_password
    from app.models import Department, Person, Project, ProjectGrp, TaskTime, ProjectType, NoWorkingDay

    # Types
    types = {}
    types['FA'] = ProjectType(typename='FA', summary='客户项目')
    types['BD'] = ProjectType(typename='BD', summary='商务拓展')
    types['Internal R&D'] = ProjectType(typename='Internal R&D', summary='内部研发')
    types['Customer Service'] = ProjectType(typename='Customer Service', summary='客户服务')
    types['Customer Product'] = ProjectType(typename='Customer Product', summary='客户产品')
    types['Other'] = ProjectType(typename='Other', summary='其他')
    for value in types.values():
        value.save()

    # Departments
    dom = parse('./app/dbdata/timesheet_departments.xml')
    assert dom.documentElement.tagName == "departments"
    elements = dom.documentElement.getElementsByTagName("dept")
    depts = {}
    for element in elements:
        dept_id = element.getAttribute('id')
        dept_name = element.getAttribute('name')
        dept_summary = element.getAttribute('summary')
        dept = Department(dept_id=dept_id, name=dept_name, summary=dept_summary)
        dept.save()
        depts[dept_id] = dept

    # Persons
    dom = parse('./app/dbdata/timesheet_persons.xml')
    assert dom.documentElement.tagName == "persons"
    elements = dom.documentElement.getElementsByTagName("person")
    for element in elements:
        username = element.getAttribute('username').strip().lower()
        fullname = element.getAttribute('fullname')
        dept_id = element.getAttribute('dept_id')
        employee_id = int(element.getAttribute('employee_id'))
        email = username + '@yashentech.com'
        user = User(username=username, email=email, password=make_password('hello'))
        user.save()

        person = Person(user=user, employee_id=employee_id,
                        privilege=1, department=depts[dept_id], display_name=fullname)
        person.save()


    # Projects
    dom = parse('./app/dbdata/timesheet_projects.xml')
    assert dom.documentElement.tagName == "projects"
    elements = dom.documentElement.getElementsByTagName("project")
    for element in elements:
        project_id = element.getAttribute('id')
        project_summary = element.getAttribute('summary')
        project_type = element.getAttribute('type')
        project = Project(project_id=project_id,
                          summary=project_summary,
                          isassociated=False, isreserved=False,
                          doclink='//fileserver2/platform/' + project_id,
                          pm=Person.objects.filter(user__username='youqi_wang')[0],
                          projecttype=types[project_type],
                          members=[],
                          completed=False)
        project.save()

    # Project group
    grp1 = ProjectGrp(grp_id='10000', summary='项目集管理',
                      owner=Person.objects.filter(user__username='youqi_wang')[0])
    grp1.save()

    # Noworkingdays
    dom = parse('./app/dbdata/timesheet_noworkingdays.xml')
    assert dom.documentElement.tagName == "noworkingdays"
    elements = dom.documentElement.getElementsByTagName("day")
    for element in elements:
        day = datetime.strptime(element.getAttribute('date'), '%Y-%m-%d')
        summary = element.getAttribute('summary')
        holiday = NoWorkingDay(date=day, summary=summary)
        holiday.save()

    print 'Database creation successful'
