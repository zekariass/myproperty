# from __future__ import absolute_import, unicode_literals

from django.conf import settings

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")


app = Celery("base")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(timezone="Europe/Paris")

app.autodiscover_tasks()
