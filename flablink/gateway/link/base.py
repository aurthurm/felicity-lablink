import threading

from abc import ABC, abstractmethod
from flablink.gateway.logger import Logger
from flablink.gateway.services.transformer import Transformer
from flablink.gateway.extensions.event.base import EventType
from flablink.gateway.extensions.event.event import post_event

logger = Logger(__name__, __file__)

class AbstractLink(ABC):

    @abstractmethod
    def start_server(self, **kwargs):
        raise NotImplementedError("start_server is not implemented")

    @abstractmethod
    def is_open(self):
        raise NotImplementedError("is_open is not implemented")

    @abstractmethod
    def is_busy(self):
        raise NotImplementedError("is_busy is not implemented")

    @abstractmethod
    def open(self):
        raise NotImplementedError("open is not implemented")

    @abstractmethod
    def close(self):
        raise NotImplementedError("close is not implemented")

    @abstractmethod
    def process(self, command):
        raise NotImplementedError("process is not implemented")

    @abstractmethod
    def get_response(self):
        raise NotImplementedError("get_response is not implemented")

    def eot_offload(self, instrument_uid, messages):
        """End of Transmission -> offload processed messages to storage"""
        logger.log("info", "Offloading to storage...")
        # Send to result repository in a new Thread
        thread = threading.Thread(target=self._push_to_order_repository,
                                    args=(instrument_uid, messages,))
        thread.start()

    def _push_to_order_repository(self, instrument_uid, messages):
        if isinstance(messages, str):
            messages = [messages]

        transformer: Transformer = Transformer()

        while len(messages) > 0:
            msg = messages.pop()
            transformer.transform_message(instrument_uid, msg)

    def show_message(self, message):
        """Prints the messaged in stdout
        """
        if not message:
            return

        logger.log("info", "-" * 80)
        logger.log("info", f"{message}")
        logger.log("info", "-" * 80)

        post_event(EventType.ACTIVITY_LOG, **{
            'id': self.uid,
            'message': message,
        })
