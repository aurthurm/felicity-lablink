from pydantic import BaseModel, validator


class InstrumentSchema(BaseModel):
    name: str
    code: str | None = None
    host: str | None = None
    port: int | None = None
    path: str | None = None
    baud_rate: int | None = None
    auto_reconnect: bool
    connection_type: str | None = None
    protocol_type: str | None = None
    socket_type: str | None = None


class InstrumentSchemaDB(InstrumentSchema):
    uid: int


class InstrumentConnection(BaseModel):
    uid: int
    action: str
