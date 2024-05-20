from typing import NoReturn
from datetime import datetime

from flablink.gateway.extensions.event.event import subscribe
from flablink.gateway.extensions.event.base import EventType
from flablink.gateway.extensions.channel.channel import broadcast
from flablink.gateway.extensions.channel.base import Channels

  
def log_activity(**kwargs) -> NoReturn:
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def stream_activity(**kwargs) -> NoReturn:
    print(kwargs)
    broadcast.publish(Channels.ACTIVITIES, kwargs)


def subscribe_felsocket_events():
    subscribe(EventType.ACTIVITY_LOG, log_activity)
    subscribe(EventType.ACTIVITY_STREAM, stream_activity)
