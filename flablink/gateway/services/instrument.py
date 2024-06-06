from flablink.gateway.models import Instrument
from flablink.gateway.services.base import BaseService

class InstrumentService(BaseService[Instrument]):
    def __init__(self):
        super().__init__(Instrument)
