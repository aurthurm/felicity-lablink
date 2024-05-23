from typing import NoReturn
from datetime import datetime

from flablink.gateway.extensions.event.event import subscribe
from flablink.gateway.extensions.event.base import EventType
from flablink.gateway.extensions.channel.channel import broadcast
from flablink.gateway.extensions.channel.base import Channels
from flablink.gateway.services.instrument import InstrumentService
from flablink.gateway.services.performance import (
    ForwarderPerfService, ForwarderService
)

instrument_service = InstrumentService()
forwarder_service = ForwarderService()
forwarder_perf_service = ForwarderPerfService()


def log_activity(**kwargs) -> NoReturn:
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def instrument_activity(**kwargs) -> NoReturn:
    kwargs["target"] = "instrument"
    broadcast.publish(Channels.ACTIVITIES, kwargs)

    if kwargs.get("id"):
        order = instrument_service.find_one(uid=kwargs.get("id"))
        instrument_service.update(
            uid=kwargs.get("id"), 
            connection=kwargs.get("connection"), 
            transmission=kwargs.get("transmission")
        )


def forward_activty(**kwargs) -> NoReturn:
    kwargs["target"] = "forwarder"
    print(kwargs)

    p = {}
    for k, v in kwargs.items():
        if isinstance(v, datetime):
            p[k] = v.strftime("%d-%m-%Y %H:%M:%S")
        else:
            p[k] = v

    broadcast.publish(Channels.ACTIVITIES, p)

    if kwargs.get("id") is None:
        # handle conecting and disconecting
        forwarder = forwarder_service.first()
        forwarder_service.update(
            uid=forwarder.uid,
            connection=kwargs.get("connection"),
            activity=kwargs.get("activity", ""),
            message=kwargs.get("message", "")
        )
    else:
        # handle activity peformance
        payload = {
            key: kwargs[key] for key in ["search_started", "search_ended", "update_started", "update_ended"] if key in kwargs
        }

        if not payload:
            return
        
        perf = forwarder_perf_service.find_one_by(order_uid=kwargs.get("id"))
        if perf:
            forwarder_perf_service.update(uid=perf.uid, **payload)
        else:
            forwarder_perf_service.create(**payload, order_uid=kwargs.get("id"))


def subscribe_felsocket_events():
    subscribe(EventType.ACTIVITY_LOG, log_activity)
    subscribe(EventType.INSTRUMENT_STREAM, instrument_activity)
    subscribe(EventType.FORWARD_STREAM, forward_activty)
