from pydantic import BaseModel


# LinkSettings
class LinkSettingsSchema(BaseModel):
    verify_results: bool
    resolve_hologic_eid: bool
    submission_limit: int
    sleep_seconds: int
    sleep_submission_count: int
    clear_data_over_days: int
    poll_db_every: int

class LinkSettingsSchemaDB(LinkSettingsSchema):
    uid: int

# LimsSettings
class LimsSettingsSchema(BaseModel):
    address: str
    api_url: str
    username: str
    password: str
    max_attempts: int
    attempt_interval: int
    is_active: bool

class LimsSettingsSchemaDB(LimsSettingsSchema):
    uid: int