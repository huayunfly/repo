# _*_ coding: utf-8 _*_
#!/usr/bin/env python
"""
Command-line utility for administrative tasks.
"""

import os
from datetime import date
import django

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
    from app.models import Department, Person, Project, ProjectGrp, TaskTime

    # using unicode as the password coding
    yun_hua = User(username='yun_hua', email='yun_hua@yashentech.com', password=make_password('hello'))
    yonghua_xu = User(username='yonghua_xu', email='yonghua_xu@yashentech.com', password=make_password('hello'))
    yinye_fan = User(username='yinye_fan', email='yinye_fan@yashentech.com', password=make_password('hello'))
    admin = User(username='admin', email='admin@yashentech.com', password=make_password('hello'))
    yun_hua.save()
    yonghua_xu.save()
    yinye_fan.save()
    admin.save()

    # yun_hua = User.objects.get(username='yun_hua')

    engineering = Department(dept_id=600800, name='技术工程部', summary='Engineering')
    engineering.save()

    # engineering = Department.objects.get(dept_id='600800')

    person1 = Person(user=yun_hua, employee_id=149, privilege=1, department=engineering)
    person1.save()
    person2 = Person(user=yonghua_xu, employee_id=61, privilege=1, department=engineering)
    person2.save()
    person3 = Person(user=yinye_fan, employee_id=99, privilege=1, department=engineering)
    person3.save()

    project1 = Project(project_id='9G90401',
                       summary='煤气化装置项目',
                       isassociated=False, isreserved=False,
                       doclink='//fileserver2/platform/9G90401',
                       pm=person1)
    project1.save()
    project2 = Project(project_id='8H10001',
                       summary='浙大八通道',
                       isassociated=False, isreserved=False,
                       doclink='//fileserver2/platform/8H10001',
                       pm=person3)
    project2.save()

    t1 = TaskTime(employee=person1, t_hours=1.0, t_percentage=0.1, workday=date.today(), project=project1)
    t1.save()
    t2 = TaskTime(employee=person1, t_hours=1.6, t_percentage=0.2, workday=date.today(), project=project2)
    t2.save()

    print 'Database creation successful'