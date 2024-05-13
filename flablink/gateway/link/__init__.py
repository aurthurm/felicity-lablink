from flablink.gateway.link.config import ConnectionType
from flablink.gateway.link.schema import InstrumentConfig
from flablink.gateway.link.serial import SerialLink
from flablink.gateway.link.socket import SocketLink


class FLabLink:
    link = None

    def __init__(self, instrument_config: InstrumentConfig):
        self.config =instrument_config

    def run(self):
        if self.config.connection_type == ConnectionType.SERIAL:
            self.link = SerialLink(self.config)
        elif self.config.connection_type == ConnectionType.TCPIP:
            self.link = SocketLink(self.config)
        
        self.link.start_server()
