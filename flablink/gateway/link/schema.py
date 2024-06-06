from pydantic import BaseModel

from flablink.gateway.link.config import ProtocolType, SocketType, ConnectionType


class InstrumentConfig(BaseModel):
    uid: int
    name: str
    code: str | None = None
    host: str | None = None
    port: int | None = None
    path: str | None = None
    baud_rate: int | None = 9600
    auto_reconnect: bool = True
    connection_type: ConnectionType | None = None
    socket_type: SocketType | None = None
    protocol_type: ProtocolType | None = None
