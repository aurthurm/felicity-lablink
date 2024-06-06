from flablink.gateway.link.base import AbstractLink
from flablink.gateway.link.schema import InstrumentConfig
from flablink.gateway.link.serial import SerialLink
from flablink.gateway.link.socket import SocketLink
from flablink.gateway.models import Instrument
from flablink.gateway.services.instrument import InstrumentService
from flablink.gateway.logger import Logger

logger = Logger(__name__, __file__)

class ConnectionService:
    def __init__(self):
        self.instrument_service = InstrumentService()

    def get_link_for(self, uid: int):
        instrument = self.instrument_service.find_one(uid)
        return self._get_link(instrument)

    def get_links(self):
        instruments = self.instrument_service.find_all()
        links = [(self._get_link(instrument)) for instrument in instruments]
        return links

    def connect(self, link: AbstractLink):
        link.start_server()
    
    def _get_link(self, instrument: Instrument):
        match instrument.connection_type:
            case "tcpip":
                return self._get_tcp_link(instrument)
            case "serial":
                return self._get_serial_link(instrument)
            case _:
                raise ValueError("Invalid connection type")

    def _get_tcp_link(self, instrument: Instrument):
        _config = InstrumentConfig(**{
            'uid': instrument.uid,
            'code': instrument.code,
            'name': instrument.name,
            'host': instrument.host,
            'port': instrument.port,
            'socket_type': instrument.socket_type,
            'protocol_type': instrument.protocol_type,
        }) 
        return SocketLink(_config)

    def _get_serial_link(self, instrument: Instrument):
        _config = InstrumentConfig(**{
            'uid': instrument.uid,
            'code': instrument.code,
            'name': instrument.name,
            'path': instrument.path,
            'baud_rate': instrument.baud_rate,
            'protocol_type': instrument.protocol_type,
        }) 
        return SerialLink(_config)
