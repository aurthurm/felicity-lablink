from pydantic import BaseModel
from flablink.gateway.schemas.instrument import InstrumentSchema


# OrderSchema
class OrderSchema(BaseModel):
    order_id: str
    test_id: str | None = None
    keywork: str
    instrument: str | None = None
    result: str
    result_date: str | None = None
    unit: str | None = None
    comment: str | None = None
    is_sync_allowed: bool
    synced: int
    sync_date: str | None = None
    sync_comment: str | None = None
    raw_message: str | None = None
    raw_data_uid: int
    instrument_uid: int | None = None

class OrderSchemaDB(OrderSchema):
    uid: int


# ResultExclusions
class ResultExclusionsSchema(BaseModel):
    result: str
    reason: str | None = None

class ResultExclusionsSchemaDB(ResultExclusionsSchema):
    uid: int


# ResultTranslation
class ResultTranslationSchema(BaseModel):
    original: str
    translated: str
    reason: str | None = None

class ResultTranslationSchemaDB(ResultTranslationSchema):
    uid: int


# KeywordMapping
class KeywordMappingSchema(BaseModel):
    keyword: str
    mappings: str
    is_active: bool

class KeywordMappingSchemaDB(KeywordMappingSchema):
    uid: int
