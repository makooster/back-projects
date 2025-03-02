import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sales_trade.settings')

celery_app = Celery('sales_trade')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()

@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    "auto-cancel-orders": {
        "task": "sales.tasks.auto_cancel_expired_orders",
        "schedule": crontab(minute="*/10"),  
    },
}
