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
from .models import ProjectGrp
from .models import FrozenDateRange


class MyAdminSite(AdminSite):
    site_header = '工时表管理控制台'


admin_site = MyAdminSite(name='Admin Console')


@admin.register(Person, site=admin_site)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department')


@admin.register(Project, site=admin_site)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'summary', 'doclink', 'pm')


@admin.register(Department, site=admin_site)
class DeptAdmin(admin.ModelAdmin):
    list_display = ('dept_id', 'name', 'summary')


@admin.register(ProjectType, site=admin_site)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ('typename', 'summary')


@admin.register(NoWorkingDay, site=admin_site)
class NoWorkingDayAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'summary')
    list_filter = ('date',)


@admin.register(ProjectGrp, site=admin_site)
class ProjectGrpAdmin(admin.ModelAdmin):
    list_display = ('grp_id', 'summary', 'owner')


@admin.register(FrozenDateRange, site=admin_site)
class FrozenDateRangeAdmin(admin.ModelAdmin):
    list_display = ('update_lt', 'update_gte', 'summary')







