from celery import Celery
from celery.schedules import crontab

app = Celery('parser', broker='redis://redis:6379/0', backend='redis://redis:6379/0', include=['main', 'script.drop_db'])
app.conf.beat_schedule = {
     'parser': {
         "task": 'main.parser',
         'schedule': crontab(hour='*/12', minute='0')
     },
     'dumper': {
         "task": 'script.drop_db.dumper',
         'schedule': crontab(hour='0', minute='0')
     }


}

app.autodiscover_tasks()
