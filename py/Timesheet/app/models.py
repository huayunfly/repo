
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

    def __unicode__(self):
        return self.dept_id

    def __str__(self):
        return self.dept_id


class Person(models.Model):
    """User scheme, extended from django User
    Default User includes username, password, email, first_name, last_name
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=120)
    privilege = models.IntegerField()
    employee_id = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    # Django will display the __str__() (__unicode__() on Python 2) of the related object.
    def __unicode__(self):
        return self.display_name

    def __str__(self):
        return self.display_name


class ProjectGrp(models.Model):
    grp_id = models.CharField(max_length=120, primary_key=True)
    summary = models.CharField(max_length=254)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, name='owner')

    def __unicode__(self):
        return self.grp_id

    def __str__(self):
        return self.grp_id


class ProjectType(models.Model):
    typename = models.CharField(max_length=50, primary_key=True)
    summary = models.CharField(max_length=254)

    def __unicode__(self):
        return self.typename

    def __str__(self):
        return self.typename


class NoWorkingDay(models.Model):
    date = models.DateField(primary_key=True)
    summary = models.CharField(max_length=254)

    def __unicode__(self):
        return self.date.isoformat()

    def __str__(self):
        return self.date.isoformat()


class Project(models.Model):
    project_id = models.CharField(max_length=120, primary_key=True)
    summary = models.CharField(max_length=254)
    isreserved = models.BooleanField(default=True)
    isassociated = models.BooleanField(default=False)
    doclink = models.CharField(max_length=516)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, name='pm')
    projectgrp = models.ForeignKey(ProjectGrp, on_delete=models.CASCADE, null=True)
    projecttype = models.ForeignKey(ProjectType, on_delete=models.CASCADE, default='FA')
    members = models.ManyToManyField(Person, related_name='members')
    completed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.project_id

    def __str__(self):
        return self.project_id


class TaskTime(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, name='employee')
    t_percentage = models.FloatField()
    t_hours = models.FloatField()
    workday = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)




