from pydantic import BaseModel

from flablink.gateway.link.config import LinkProtocol, SocketType, ConnectionType


class InstrumentConfig(BaseModel):
    uid: str
    name: str
    code: str | None
    host: str | None
    port: int | None
    path: str | None
    baud_rate: int | None = 9600
    auto_reconnect: bool = True
    connection_type: ConnectionType | None
    socket_type: SocketType | None
    protocol_type: LinkProtocol | None
