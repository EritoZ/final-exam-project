import os
from celery import Celery

from DjangoForum import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoForum.settings')

app = Celery('DjangoForum')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)