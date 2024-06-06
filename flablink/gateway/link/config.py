from enum import StrEnum


class NotConnectedException(Exception):
        pass


class ConnectionType(StrEnum):
    SERIAL = 'serial'
    TCPIP = 'tcpip'


class SocketType(StrEnum):
    CLIENT = 'client'
    SERVER = 'server'


class ProtocolType(StrEnum):
    HL7 = 'hl7'
    ASTM = 'astm'

