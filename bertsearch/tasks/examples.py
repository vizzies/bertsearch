from celery.signals import setup_logging, celeryd_init
from bertsearch.extensions import celery

@celery.task(bind=True)
def example1(self):

    celery_task = self

    print("Hello, world from Celery")
    
    return "Done"