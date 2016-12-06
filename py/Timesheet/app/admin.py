# -*- coding: utf-8 -*-
"""
Definition of admin
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Project
from .models import Person
from .models import Department
from .models import ProjectType
from .models import NoWorkingDay


class MyAdminSite(AdminSite):
    site_header = 'Timesheet管理控制台'


admin_site = MyAdminSite(name='Admin Console')


@admin.register(Person, site=admin_site)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Project, site=admin_site)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Department, site=admin_site)
class DeptAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectType, site=admin_site)
class ProjectTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(NoWorkingDay, site=admin_site)
class NoWorkingDayAdmin(admin.ModelAdmin):
    pass





