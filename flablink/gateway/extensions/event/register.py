# init events on app start app
from flablink.gateway.events import subscribe_felsocket_events


def observe_events():
    subscribe_felsocket_events()
