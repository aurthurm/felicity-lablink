# -*- coding: utf-8 -*-

from flablink.gateway.logger import Logger
from flablink.gateway.services.order import OrderService
from flablink.gateway.adapters import MessageAdapter

logger = Logger(__name__, __file__)


class Transformer: # previously OrderService

    def __init__(self):
        self._converter = None
        self._order_service = None

    def transform_message(self, instrument_uid, message):
        # persist raw_data
        rawdata_uid = self.order_service.persist_raw(instrument_uid, message)

        payloads = self.adapter.process(message)
        if isinstance(payloads, dict):
            payloads = [payloads]

        # persist message splits as orders
        for payload in payloads:
            order = self._to_order(payload)
            order_id = order.get("order_id", None)
            order_result = order.get("result", None)
            logger.log(
                "info", f"order for db:: order_id -> {order_id} -> result -> {order_result}")
            self.order_service.persist_order(instrument_uid, order, rawdata_uid)

    def handle_replay(self, raw_data):
        payloads = self.adapter.process(raw_data.content)
        if isinstance(payloads, dict):
            payloads = [payloads]

        # persist message splits as orders
        for order in payloads:
            order = self._to_order(order)
            order_id = order.get("order_id", None)
            order_result = order.get("result", None)
            logger.log(
                "info", f"order for db:: order_id -> {order_id} -> result -> {order_result}")
            self.order_service.persist_order(order, raw_data.uid)

    def update_fix(self, raw_data):
        """For updating old messages fix"""
        payloads = self.adapter.process(raw_data.content)
        if isinstance(payloads, dict):
            payloads = [payloads]

        # persist message splits as orders
        for order in payloads:
            order = self._to_order(order)
            logger.log("info", f"order for update: {order}")
            self.order_service.update_order_fix({
                "order_id": order['order_id'],
                "result": order['result'],
                "raw_message": order['raw_message']
            }, raw_data.uid)

    @staticmethod
    def _to_order(message):
        id = message.get("id")
        return {
            "order_id": id,
            "test_id": id,
            "keywork": message.get("keyword"),
            "result": message.get("result"),
            "result_date": message.get("capture_date"),
            "raw_message": message.get("raw_message")
        }

    @property
    def order_service(self):
        if not self._order_service:
            self._order_service = OrderService()
        return self._order_service

    @property
    def adapter(self): # previously converter
        if not self._converter:
            self._converter = MessageAdapter()
        return self._converter
