from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from flablink.gateway.db.session import job_store
from datetime import datetime

from flablink.gateway.services.connection import ConnectionService

global scheduler
scheduler = BackgroundScheduler()
# scheduler.add_jobstore(job_store, 'sqlalchemy')


def job_listener(event):
    global scheduler
    if event.exception:
        print(f'Job {event.job_id} failed')
    else:
        print(f'Job {event.job_id} completed successfully')

    # Reschedule the job after completion or failure
    link = ConnectionService().get_link_for(int(event.job_id))
    scheduler.add_job(link.start_server, next_run_time=datetime.now(), id=event.job_id, replace_existing=True) # , jobstore='sqlalchemy'


def start_scheduler():
    global scheduler
    links = ConnectionService().get_links()
    for link in links:
        print(link.__dict__)
        scheduler.add_job(link.start_server, next_run_time=datetime.now(), id=str(link.uid), replace_existing=True) # , jobstore='sqlalchemy'

    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()

def shutdown_scheduler():
    global scheduler
    scheduler.shutdown(wait=False)
