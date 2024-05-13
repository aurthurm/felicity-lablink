from typing import Dict

from fastapi import Depends

from flablink.gateway.extensions.event.base import EventType
from flablink.gateway.extensions.event.event import post_event
from flablink.gateway.link.schema import InstrumentConfig
from flablink.gateway.link.socket import  InstrumentMLLP
from flablink.gateway.models import Instrument
from flablink.gateway.services.instrument import InstrumentService


class ConnectionService:
    def __init__(self, instrument_service: InstrumentService = Depends()):
        self.instrument_service = instrument_service
        self.sessions: Dict[str, InstrumentMLLP] = {}

    def initialise(self):
        instruments = self.instrument_service.find_all()
        for _inst in instruments:
            self._add_session(_inst)

        self.connect_all()

    def connect_all(self):
        for _key in self.sessions.keys():
            self.sessions[_key].connect()

    def add(self, instrument_uid: str):
        instrument = self.instrument_service.find_one(instrument_uid)
        self._add_session(instrument)

    def remove(self, instrument_uid: str):
        self._remove_session(instrument_uid)
    
    def _add_session(self, instrument: Instrument):
        if instrument.uid not in self.sessions or instrument.auto_reconnect:
            post_event(EventType.ACTIVITY_STREAM, {
                'id': instrument.uid,
                'message': 'connecting',
                'connecting': True,
                'connected': False,
            })

            match instrument.connection_type:
                case "tcpip":
                    self._init_tcpip_connection(instrument)
                case "serial":
                    self._init_serial_connections(instrument)

    def _remove_session(self, instrument_uid: str):
        if instrument_uid in self.sessions:
            self.sessions[instrument_uid].close()
            del self.sessions[instrument_uid]

            post_event(EventType.ACTIVITY_STREAM, {
                'id': instrument_uid,
                'message': 'disconnected',
                'connecting': False,
                'connected': False,
            })

    def _init_tcpip_connection(self, instrument: Instrument):
        _config = InstrumentConfig({
            'name': instrument.name,
            'address': instrument.host,
            'port': instrument.port,
            'connection_type': instrument.connection_type,
            'protocol': instrument.protocol,
        }) 
        self.sessions[instrument.uid] = InstrumentMLLP(_config)

    def _init_serial_connections(self, instrument: Instrument):
        ...