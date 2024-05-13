import logging

from typing import NoReturn
from datetime import datetime

from flablink.gateway.extensions.event.event import subscribe
from flablink.gateway.extensions.event.base import EventType

  
def log_activity(source: str, message: str, **kwargs) -> NoReturn:
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    logger = logging.getLogger(source)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.FileHandler(f"{source}.log"))
    logger.info(f"{now}: <{source}> : {message}")


def stream_activity(payload: str, **kwargs) -> NoReturn:
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(payload)


def subscribe_felsocket_events():
    subscribe(EventType.ACTIVITY_LOG, log_activity)
    subscribe(EventType.ACTIVITY_STREAM, stream_activity)
