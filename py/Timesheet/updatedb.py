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
    from app.models import Department, Person, Project, ProjectGrp, \
        TaskTime, ProjectType, NoWorkingDay, FrozenDateRange

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
    admin_dept = Department(dept_id=600310, name='行政部', summary='Admin')
    admin_dept.save()

    # engineering = Department.objects.get(dept_id='600800')

    person1 = Person(user=yun_hua, employee_id=149, privilege=1, department=engineering, display_name='花云')
    person1.save()
    person2 = Person(user=yonghua_xu, employee_id=61, privilege=1, department=engineering, display_name='徐勇华')
    person2.save()
    person3 = Person(user=yinye_fan, employee_id=99, privilege=1, department=engineering, display_name='范寅烨')
    person3.save()
    person_admin = Person(user=admin, employee_id=0, privilege=1, department=engineering, display_name='Admin')
    person_admin.save()

    type1 = ProjectType(typename='FA', summary='客户项目')
    type1.save()
    type2 = ProjectType(typename='BD', summary='商务拓展')
    type2.save()
    type3 = ProjectType(typename='Internal R&D', summary='内部研发')
    type3.save()
    type4 = ProjectType(typename='customer service', summary='客户服务')
    type4.save()
    type5 = ProjectType(typename='Other', summary='其他')
    type5.save()

    grp1 = ProjectGrp(grp_id='10000', summary='项目集管理', owner=person_admin)
    grp1.save()

    project1 = Project(project_id='9G90401',
                       summary='煤气化装置项目',
                       isassociated=False, isreserved=False,
                       doclink='//fileserver2/platform/9G90401',
                       pm=person1,
                       projecttype=type1,
                       members=[person1, person2])
    project1.save()
    project2 = Project(project_id='8H10001',
                       summary='浙大八通道',
                       isassociated=False, isreserved=False,
                       doclink='//fileserver2/platform/8H10001',
                       pm=person3,
                       projecttype=type1)
    project2.save()
    project3 = Project(project_id='有薪假',
                       summary='Paid leave',
                       isassociated=False, isreserved=False,
                       doclink='//fileserver/Devision/HR',
                       pm=person_admin,
                       projecttype=type5)
    project3.save()

    t1 = TaskTime(employee=person1, t_hours=1.0, t_percentage=0.1, workday=date.today(), project=project1)
    t1.save()
    t2 = TaskTime(employee=person1, t_hours=1.6, t_percentage=0.2, workday=date.today(), project=project2)
    t2.save()
    t3 = TaskTime(employee=person1, t_hours=1.6, t_percentage=0.2, workday=date.today(), project=project3)
    t3.save()

    holiday1 = NoWorkingDay(date=date(year=2016, month=12, day=3), summary='Weekend')
    holiday1.save()
    holiday2 = NoWorkingDay(date=date(year=2016, month=12, day=4), summary='Weekend')
    holiday2.save()
    holiday3 = NoWorkingDay(date=date(year=2016, month=12, day=10), summary='Weekend')
    holiday3.save()
    holiday4 = NoWorkingDay(date=date(year=2016, month=12, day=11), summary='Weekend')
    holiday4.save()

    frozen_range = FrozenDateRange(update_gte=date(1970, 1, 1),
                                   update_lt=date(2016, 11, 1), summary='冻结修改期限')
    frozen_range.save()

    print 'Database creation successful'
