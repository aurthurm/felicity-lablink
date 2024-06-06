from sqlalchemy import Column, Integer, String, Boolean, Index

from flablink.gateway.db.base_model import DBModel


class LinkSettings(DBModel):
    __tablename__ = "link_settings"
    __table_args__ = {'extend_existing': True}

    # General settings
    verify_results = Column(Boolean, default=False) # auto verify results after submission
    resolve_hologic_eid = Column(Boolean, default=False)
    submission_limit = Column(Integer, default=250) # number of results to get from db for submissions at a time
    sleep_seconds = Column(Integer, default=5) # sleep seconds before next submission to api
    sleep_submission_count = Column(Integer, default=10) # sleep after submission count and continue
    clear_data_over_days = Column(Integer, default=30)
    poll_db_every = Column(Integer, default=10)


class LimsSettings(DBModel):
    __tablename__ = "lims_settings"
    __table_args__ = {'extend_existing': True}

    # Database settings
    address = Column(String(100))
    api_url = Column(String(100), unique=False, default="/senaite/@@API/senaite/v1")
    username =  Column(String(50), unique=False, default="system_daemon")
    password =  Column(String(50), unique=False, default="s89Ajs-UIas!3k")
    max_attempts = Column(Integer, default=10)
    attempt_interval = Column(Integer, default=30)
    is_active = Column(Boolean, nullable=False)

