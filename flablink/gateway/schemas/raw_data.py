from pydantic import BaseModel

from flablink.gateway.schemas.instrument import InstrumentSchema


class RawDataSchema(BaseModel):
    uid: int
    content: str    
    instrument_uid: int | None = None
    instrument: InstrumentSchema | None = None