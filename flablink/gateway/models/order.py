from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String, Boolean, UniqueConstraint
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship

from flablink.gateway.db.base_model import DBModel


class Order(DBModel):
    __tablename__ = "orders"
    __table_args__ = {'extend_existing': True}

    order_id = Column(String(50), nullable=False)
    test_id = Column(String(50), nullable=True)
    keywork = Column(String(50), nullable=False)
    instrument = Column(String(50), nullable=True)
    result = Column(String(255), nullable=False)
    result_date = Column(String(25), nullable=False)
    unit = Column(String(20), nullable=True)
    comment = Column(String(255), nullable=True)
    is_sync_allowed = Column(Boolean, nullable=False, default=True)
    synced = Column(SmallInteger, nullable=False, default=False)
    sync_date = Column(String(25), nullable=True)
    sync_comment = Column(String(255), nullable=True)
    raw_message = Column(LONGTEXT, nullable=True)
    raw_data_uid = Column(
        Integer,
        ForeignKey("raw_data.uid", ondelete="CASCADE"),
        nullable=False
    )
    instrument_uid = Column(
        Integer,
        ForeignKey("instruments.uid", ondelete="CASCADE"),
        nullable=True
    )



class ResultExclusions(DBModel):
    __tablename__ = 'result_exclusions'
    __table_args__ = {'extend_existing': True}

    result = Column(String(100), unique=True)
    reason = Column(String(255), nullable=True)


class ResultTranslation(DBModel):
    __tablename__ = 'result_translations'
    __table_args__ = {'extend_existing': True}

    original = Column(String(100))
    translated = Column(String(100))
    reason = Column(String(255), nullable=True)

    __table_args__ = (
        UniqueConstraint('original', 'translated'),
    )


class KeywordMapping(DBModel):
    __tablename__ = 'lims_keywords'
    __table_args__ = {'extend_existing': True}

    keyword = Column(String(50), unique=True)
    mappings = Column(String(255))
    is_active = Column(Boolean, default=False)