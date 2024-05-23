from pydantic import BaseModel


# ForwarderSchema
class ForwarderSchema(BaseModel):
    connection: str | None = None
    activity: str | None = None
    message: str | None = None

class ForwarderSchemaDB(ForwarderSchema):
    uid: int
    created_at: str
    updated_at: str


# ForwarderPerfSchema
class ForwarderPerfSchema(BaseModel):
    search_started: str | None = None
    search_ended: str | None = None
    update_started: str | None = None
    update_ended: str | None = None
    message: str | None = None
    order_uid: int

class ForwarderPerfSchemaDB(ForwarderPerfSchema):
    uid: int
    created_at: str
    updated_at: str
