from datetime import datetime, timedelta

from fastapi import Depends

from flablink.gateway.models import (
    Order,
    ResultExclusions,
    ResultTranslation,
    KeywordMapping
)
from flablink.gateway.logger import Logger
from flablink.gateway.helpers import has_special_char
from flablink.config import DB_CLEAR_DATA_OVER_DAYS
from flablink.gateway.services.base import BaseService
from flablink.gateway.services.raw_data import RawDataService


logger = Logger(__name__, __file__)


def sanitise(incoming):
    incoming = list(incoming)
    for index, item in enumerate(incoming):
        if isinstance(item, str):
            incoming[index] = item.replace(';', ' ').strip()
    return incoming


class OrderService(BaseService[Order]):
    def __init__(self):
        self.raw_data_service = RawDataService()
        super().__init__(Order)
    
    def clean(self):
        cutoff_date = datetime.now() - timedelta(days=DB_CLEAR_DATA_OVER_DAYS)
        logger.log("info", 
                   f"OrderService: cleaning raw messages and orders greater than {cutoff_date} == {DB_CLEAR_DATA_OVER_DAYS} days ago...")
        raws = self.raw_data_service.find_all(filters={"created_at__le": cutoff_date})
        for raw in raws:
            orders = self.model.get_all(raw_data_uid=raw.uid)
            for order in orders:
                order.delete()
            raw.delete()
        logger.log("info", "OrderService: cleaning complete")

    def persist_raw(self, instrument_uid: int, message: str):
        return self.raw_data_service.persist_raw(instrument_uid, message)

    def persist_order(self, instrument_uid: int, order: Order, raw_data_uid: int):
        order_id = order.get("order_id")
        result_date = order.get("result_date")
        filters = {
            'order_id': order_id,
            'result_date': result_date
        }
        found = self.model.get(**filters)
        if found:
            # EID do repeat so need some hack to save more here

            #
            logger.log(
                "info", f"order with the same order_id ({order_id}) resulted ({result_date}) is already persisted, skipping ...")
            return

        hspc = has_special_char(order_id)
        self.model.create(**{
            "instrument_uid": instrument_uid,
            "raw_data_uid": raw_data_uid,
            **order,
            "synced": 2 if hspc else 0,
            "sync_comment": "Incorrect Sample Id" if hspc else None
        })

    def update_order_fix(self, order: Order, raw_data_uid: int):
        order_id = order["order_id"]
        filters = {
            'order_id': order_id
        }
        found = self.model.get(**filters)
        if not found:
            logger.log(
                "info", f"order with the same order_id ({order_id}) is does not exist, skipping ...")
            return

        hspc = has_special_char(order_id)
        found.update(**{
            "raw_data_uid": raw_data_uid,
            **order,
            "synced": 2 if hspc else 0,
            "sync_comment": "Incorrect Sample Id" if hspc else None
        })


class ResultExclusionsService(BaseService[ResultExclusions]):
    def __init__(self):
        super().__init__(ResultExclusions)


class ResultTranslationService(BaseService[ResultTranslation]):
    def __init__(self):
        super().__init__(ResultTranslation)


class KeywordMappingService(BaseService[KeywordMapping]):
    def __init__(self):
        super().__init__(KeywordMapping)
