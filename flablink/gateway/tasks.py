from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.triggers.cron import CronTrigger

from flablink.gateway.db.session import job_store
from flablink.gateway.services.connection import ConnectionService
from flablink.gateway.forward.engine import ResultFowarder
from flablink.gateway.services.order.order import OrderService
from flablink.gateway.forward.conf import LINK_SETTINGS

from flablink.gateway.logger import Logger

logger = Logger(__name__, __file__)

global scheduler
scheduler = BackgroundScheduler()
# scheduler.add_jobstore(job_store, 'sqlalchemy')
forwader = ResultFowarder()
order_service = OrderService()
trigger = CronTrigger(hour=2, minute=0)  # 2:00 AM every day


def job_listener(event):
    global scheduler
    if event.exception:
        print(f'Job {event.job_id} failed')
        if event.job_id == "result_forwarder":
            scheduler.add_job(forwader.run, 'interval', minutes=LINK_SETTINGS.poll_db_every, id=event.job_id, replace_existing=True)
            return
        
        if event.job_id == "order_cleaner": 
            scheduler.add_job(order_service.clean, trigger=trigger, id=event.job_id, replace_existing=True)
            return
    else:
        print(f'Job {event.job_id} completed successfully')

    # Reschedule the job after completion or failure
    if event.job_id not in ["result_forwarder", "order_cleaner"]:
        link = ConnectionService().get_link_for(int(event.job_id))
        scheduler.add_job(link.start_server, next_run_time=datetime.now(), id=event.job_id, replace_existing=True) # , jobstore='sqlalchemy'


def start_scheduler():
    global scheduler
    links = ConnectionService().get_links()
    # add instrument connection jobs
    for link in links:
        print(link.__dict__)
        scheduler.add_job(link.start_server, next_run_time=datetime.now(), id=str(link.uid), replace_existing=True) # , jobstore='sqlalchemy'
    # add result foward job
    scheduler.add_job(forwader.run, 'interval', minutes=1, id="result_forwarder", replace_existing=True) # , jobstore='sqlalchemy'
    # add order cleaner
    scheduler.add_job(order_service.clean, trigger=trigger, id="order_cleaner", replace_existing=True) # , jobstore='sqlalchemy'
    # add job listener
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    # run scheduler
    scheduler.start()

def shutdown_scheduler():
    global scheduler
    scheduler.shutdown(wait=False)
