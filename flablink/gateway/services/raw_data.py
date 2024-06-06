from flablink.gateway.models import RawData
from flablink.gateway.logger import Logger
from flablink.gateway.services.base import BaseService

logger = Logger(__name__, __file__)


class RawDataService(BaseService[RawData]):
    def __init__(self):
        super().__init__(RawData)
    
    def persist_raw(self, instrument_uid: int, message: str):
        raw_data = self.model.create(**{
            "instrument_uid": instrument_uid,
            "content": str(message)
        })
        return raw_data.uid
