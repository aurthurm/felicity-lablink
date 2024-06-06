from flablink.gateway.models.performance import Forwarder, ForwarderPerf
from flablink.gateway.services.base import BaseService


class ForwarderService(BaseService[Forwarder]):
    def __init__(self):
        super().__init__(Forwarder)


class ForwarderPerfService(BaseService[ForwarderPerf]):
    def __init__(self):
        super().__init__(ForwarderPerf)
