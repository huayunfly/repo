"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.models import TaskTime
from app.models import Project
from app.models import Person

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


def timeline(request, date):
    """Renders the timeline page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/timeline.html',
        {
            'title': 'About',
            'message': 'Your timeline page',
            'year': datetime.now().year,
            'tasks': TaskTime.objects.filter(employee__user__username=request.user.username),
        }
    )