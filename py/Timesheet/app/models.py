
"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Department(models.Model):
    dept_id = models.CharField(primary_key=True, max_length=120)
    name = models.CharField(max_length=120)
    summary = models.CharField(max_length=254)


class Person(models.Model):
    """User scheme, extended from django User
    Default User includes username, password, email, first_name, last_name
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    privilege = models.IntegerField()
    employee_id = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


class ProjectGrp(models.Model):
    grp_id = models.CharField(max_length=120, primary_key=True)
    summary = models.CharField(max_length=254)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, name='owner')


class ProjectType(models.Model):
    typename = models.CharField(max_length=50, primary_key=True)
    summary = models.CharField(max_length=254)


class NoWorkingDay(models.Model):
    date = models.DateField(primary_key=True)
    summary = models.CharField(max_length=254)


class Project(models.Model):
    project_id = models.CharField(max_length=120, primary_key=True)
    summary = models.CharField(max_length=254)
    isreserved = models.BooleanField()
    isassociated = models.BooleanField()
    doclink = models.CharField(max_length=516)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, name='pm')
    projectgrp = models.ForeignKey(ProjectGrp, on_delete=models.CASCADE, null=True)
    projecttype = models.ForeignKey(ProjectType, on_delete=models.CASCADE, default='FA')
    members = models.ManyToManyField(Person, related_name='members')


class TaskTime(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, name='employee')
    t_percentage = models.FloatField()
    t_hours = models.FloatField()
    workday = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)




