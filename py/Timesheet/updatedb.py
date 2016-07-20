#!/usr/bin/env python
"""
Command-line utility for administrative tasks.
"""

import os
import django

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Timesheet.settings")
    django.setup()

    from app.models import Department
    d1 = Department(dept_id=600800, name='Engineering', summary='Engineering')
    d1.save()
    print Department.objects.all()