from __future__ import absolute_import
import os
from celery import Celery

from market_place import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_place.settings')
app = Celery("market_place")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# @app.task
# def add(x, y):
#     return x / y
