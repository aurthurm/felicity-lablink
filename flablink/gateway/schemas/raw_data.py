from pydantic import BaseModel


class RawDataSchemaOut(BaseModel):
    uid: str
    content: str    
    instrument_uid: str | None