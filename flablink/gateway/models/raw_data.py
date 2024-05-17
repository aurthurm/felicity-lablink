from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship

from flablink.gateway.db.base_model import DBModel


class RawData(DBModel):
    __tablename__ = "raw_data"
    __table_args__ = {'extend_existing': True}

    content = Column(LONGTEXT, nullable=False)    
    instrument_uid = Column(
        Integer,
        ForeignKey("instruments.uid", ondelete="CASCADE"),
        nullable=True
    )
    instrument = relationship("Instrument", lazy="selectin")