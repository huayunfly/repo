"""
Definition of urls for Timesheet.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views
from app.utils.timekit import monthweek

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact/$', app.views.contact, name='contact'),
    url(r'^about/$', app.views.about, name='about'),
    url(r'^thanks/$', app.views.thanks, name='thanks'),
    url(r'error/$', app.views.error, name='error'),
    url(r'^timeline/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<week>[0-6]{1})/$', app.views.timeline, name='timeline'),

    # Here's what django.contrib.auth.views.login does:
    # If called via GET, it displays a login form that POSTs to the same URL. More on this in a bit.
    # If called via POST with user submitted credentials, it tries to log the user in. If login is successful,
    # the view redirects to the URL specified in next.
    # If next isn't provided, it redirects to settings.LOGIN_REDIRECT_URL (which defaults to /accounts/profile/).
    # If login isn't successful, it redisplays the login form.

    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
                'currentweek': '/timeline/%d/%02d/%d/' %
                (datetime.now().year, datetime.now().month, monthweek(datetime.now())),
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
