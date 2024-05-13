import threading

from abc import ABCMeta, abstractmethod
from flablink.gateway.logger import Logger
from flablink.gateway.services.transformer import Transformer

logger = Logger(__name__, __file__)


class AbstractLink(ABCMeta):

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

    def handle_eot(self, messages):
        # Send to result repository in a new Thread
        thread = threading.Thread(target=self.push_to_order_repository,
                                    args=(messages,))
        thread.start()

    def push_to_order_repository(self, messages):
        if isinstance(messages, str):
            messages = [messages]

        transformer: Transformer = Transformer()

        while len(messages) > 0:
            msg = messages.pop()
            transformer.transform_message(msg)

    def show_message(self, message):
        """Prints the messaged in stdout
        """
        if not message:
            return

        print("-" * 80)
        print(message)
        print("-" * 80)