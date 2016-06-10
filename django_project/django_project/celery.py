from __future__ import absolute_import

import os
from datetime import timedelta

from celery import Celery
from celery.decorators import periodic_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

from django.conf import settings

app = Celery('django_project')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.LOCAL_APPS)


@app.task(bind=True)
def debug_task(self):
	print('Request: {}'.format(self.request))


