from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from flablink.gateway.db.base_model import DBModel


class Forwarder(DBModel):
    __tablename__ = "forwarder"
    __table_args__ = {'extend_existing': True}

    connection = Column(String(20), nullable=False) # connected, disconnected, error
    activity = Column(String(20), nullable=True) # 
    message = Column(String(255), nullable=True) # any message


class ForwarderPerf(DBModel):
    __tablename__ = "forwarder_perf"
    __table_args__ = {'extend_existing': True}

    search_started = Column(DateTime, nullable=True)
    search_ended = Column(DateTime, nullable=True)
    update_started = Column(DateTime, nullable=True)
    update_ended = Column(DateTime, nullable=True)
    message = Column(String(255), nullable=True) # any message
    order_uid = Column(
        Integer,
        ForeignKey("orders.uid", ondelete="CASCADE"),
        nullable=False
    )
