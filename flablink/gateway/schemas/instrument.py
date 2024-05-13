from pydantic import BaseModel


class RawDataSchemaOut(BaseModel):
    uid: str
    content: str    
    instrument_uid: str | None


class InstrumentSchema(BaseModel):
    uid: str
    name: str
    code: str | None
    host: str | None
    port: int | None
    path: str | None
    baud_rate: int | None
    auto_reconnect: bool
    connection_type: str | None
    protocol_type: str | None
    socket_type: str | None

