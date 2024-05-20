from typing import Optional
from pydantic import BaseModel, ConfigDict
from flablink.gateway.schemas.instrument import InstrumentSchema


# OrderSchema
class OrderSchema(BaseModel):
    order_id: str
    test_id: Optional[str] = None
    keyword: str
    instrument: Optional[str] = None
    result: str
    result_date: Optional[str] = None
    unit: Optional[str] = None
    comment: Optional[str] = None
    is_sync_allowed: bool
    synced: int
    sync_date: Optional[str] = None
    sync_comment: Optional[str] = None
    raw_message: Optional[str] = None
    raw_data_uid: int
    instrument_uid: Optional[int] = None

class OrderSchemaDB(OrderSchema):
    uid: int
    created_at: str
    updated_at: str


# ResultExclusions
class ResultExclusionsSchema(BaseModel):
    result: str
    reason: Optional[str] = None

class ResultExclusionsSchemaDB(ResultExclusionsSchema):
    uid: int
    model_config = ConfigDict(from_attributes=True)


# ResultTranslation
class ResultTranslationSchema(BaseModel):
    original: str
    translated: str
    reason: Optional[str] = None

class ResultTranslationSchemaDB(ResultTranslationSchema):
    uid: int
    model_config = ConfigDict(from_attributes=True)


# KeywordMapping
class KeywordMappingSchema(BaseModel):
    keyword: str
    mappings: str
    is_active: bool

class KeywordMappingSchemaDB(KeywordMappingSchema):
    uid: int
    model_config = ConfigDict(from_attributes=True)
