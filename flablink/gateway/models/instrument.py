from sqlalchemy import Column, Integer, String, Boolean

from flablink.gateway.db.base_model import DBModel


class Instrument(DBModel):
    __tablename__ = "instruments"
    __table_args__ = {'extend_existing': True}

    name = Column(String(30)) # instrument name
    code = Column(String(10), nullable=True) # instrument code
    host = Column(String(100), nullable=True) # ip address
    port = Column(Integer, nullable=True) # tcp port
    path = Column(String(20), nullable=True) # serial port path
    baud_rate = Column(Integer, nullable=True) # serial port baud rate
    auto_reconnect = Column(Boolean, default=True) # auto reconnect on connection lost
    connection_type = Column(String(10), nullable=True) # tcpip, serial
    protocol_type = Column(String(10), nullable=True) # astm, hl7
    socket_type = Column(String(10), nullable=True) # client or server
    # connection status upated by the gateway
    connection = Column(String(20), default="disconnected") # connected, disconnected
    transmission = Column(String(20), default="")  # "ended" ?? mabe not needed
