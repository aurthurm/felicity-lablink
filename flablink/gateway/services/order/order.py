from datetime import datetime, timedelta

from sqlalchemy import select, func, text
from sqlalchemy.orm import Session
from flablink.gateway.models import Order
from flablink.gateway.logger import Logger
from flablink.gateway.helpers import has_special_char
from flablink.gateway.forward.conf import LINK_SETTINGS
from flablink.gateway.services.base import BaseService
from flablink.gateway.services.raw_data import RawDataService
from flablink.gateway.db.session import engine


logger = Logger(__name__, __file__)


def sanitise(incoming):
    incoming = list(incoming)
    for index, item in enumerate(incoming):
        if isinstance(item, str):
            incoming[index] = item.replace(';', ' ').strip()
    return incoming


class OrderService(BaseService[Order]):
    def __init__(self):
        self.raw_data_service = RawDataService()
        super().__init__(Order)
    
    def clean(self):
        cutoff_date = datetime.now() - timedelta(days=LINK_SETTINGS.clear_data_over_days)
        logger.log("info", 
                   f"OrderService: cleaning raw messages and orders greater than {cutoff_date} == {LINK_SETTINGS.clear_data_over_days} days ago...")
        raws = self.raw_data_service.find_all(filters={"created_at__le": cutoff_date})
        for raw in raws:
            orders = self.model.get_all(raw_data_uid=raw.uid)
            for order in orders:
                order.delete()
            raw.delete()
        logger.log("info", "OrderService: cleaning complete")

    def persist_raw(self, instrument_uid: int, message: str):
        return self.raw_data_service.persist_raw(instrument_uid, message)

    def persist_order(self, instrument_uid: int, order: Order, raw_data_uid: int):
        order_id = order.get("order_id")
        result_date = order.get("result_date")
        filters = {
            'order_id': order_id,
            'result_date': result_date
        }
        found = self.model.get(**filters)
        if found:
            # EID do repeat so need some hack to save more here

            #
            logger.log(
                "info", f"order with the same order_id ({order_id}) resulted ({result_date}) is already persisted, skipping ...")
            return

        hspc = has_special_char(order_id)
        self.model.create(**{
            "instrument_uid": instrument_uid,
            "raw_data_uid": raw_data_uid,
            **order,
            "synced": 2 if hspc else 0,
            "sync_comment": "Incorrect Sample Id" if hspc else None
        })

    def update_order(self, uid, order: dict):
        found = self.model.get(uid=uid)
        if not found:
            logger.log("info", f"order with the same uid ({uid}) is does not exist, skipping ...")
            return

        hspc = has_special_char(order.get("order_id", ""))
        found.update(**{
            **order,
            "synced": 2 if hspc else 0,
            "sync_comment": "Incorrect Sample Id" if hspc else None
        })

    def statistics(self):
        stats = {}
        with Session(engine) as session:
            results = session.execute(
                select(
                    self.model.synced, 
                    func.count().label('total')
                ).group_by(self.model.synced)
            )
            stats["sync"] = results.all()
            results = session.execute(
                select(
                    self.model.instrument_uid,
                    func.timestampdiff(text('MINUTE'), func.max(self.model.created_at), func.current_timestamp()).label('minutes_ago')
                ).group_by(
                    self.model.instrument_uid
                )
            )
            stats["last_creation"] = results.all()
            results = session.execute(
                select(func.max(self.model.sync_date)).filter(self.model.sync_date != None)
            )
            stats["last_sync"] = results.scalar()
        

        created_hourly = session.query(
            func.date_format(self.model.created_at, '%Y-%m-%d %H').label('hour'),
            self.model.instrument_uid,
            func.count().label('count')
        ).filter(
            self.model.created_at >= func.now() - text('interval 24 hour')
        ).group_by(
            func.date_format(self.model.created_at, '%Y-%m-%d %H'),
            self.model.instrument_uid,
        ).order_by(
            func.date_format(self.model.created_at, '%Y-%m-%d %H'),
            self.model.instrument_uid,
        )

        created_daily = session.query(
            func.date_format(self.model.created_at, '%Y-%m-%d').label('date'),
            self.model.instrument_uid,
            func.count().label('count')
        ).filter(
            self.model.created_at >= func.now() - text('interval 7 day')
        ).group_by(
            func.date_format(self.model.created_at, '%Y-%m-%d'),
            self.model.instrument_uid,
        ).order_by(
            func.date_format(self.model.created_at, '%Y-%m-%d'),
            self.model.instrument_uid,
        )

        created_weekly = session.query(
            func.date_format(self.model.created_at, '%Y-%m-%W').label('week'),
            self.model.instrument_uid,
            func.count().label('count')
        ).filter(
            self.model.created_at >= func.now() - text('interval 30 day')
        ).group_by(
            func.date_format(self.model.created_at, '%Y-%m-%W'),
            self.model.instrument_uid,
        ).order_by(
            func.date_format(self.model.created_at, '%Y-%m-%W'),
            self.model.instrument_uid,
        )

        with Session(engine) as session:
            results = session.execute(created_hourly)
            stats["created_hourly"] = results.all()
            results = session.execute(created_daily)
            stats["created_daily"] = results.all()
            results = session.execute(created_weekly)
            stats["created_weekly"] = results.all()

        synced_hourly = session.query(
            func.date_format(self.model.sync_date, '%Y-%m-%d %H').label('hour'),
            self.model.instrument_uid,
            func.count().label('count')
        ).filter(
            self.model.sync_date >= func.now() - text('interval 24 hour'),
            self.model.synced > 0
        ).group_by(
            func.date_format(self.model.sync_date, '%Y-%m-%d %H'),
            self.model.instrument_uid,
        ).order_by(
            func.date_format(self.model.sync_date, '%Y-%m-%d %H'),
            self.model.instrument_uid,
        )
        synced_daily = session.query(
            func.date_format(self.model.sync_date, '%Y-%m-%d').label('date'),
            self.model.instrument_uid,
            func.count().label('count')
        ).filter(
            self.model.sync_date >= func.now() - text('interval 7 day'),
            self.model.synced > 0
        ).group_by(
            func.date_format(self.model.sync_date, '%Y-%m-%d'),
            self.model.instrument_uid,
        ).order_by(
            func.date_format(self.model.sync_date, '%Y-%m-%d'),
            self.model.instrument_uid,
        )

        synced_weekly = session.query(
            func.date_format(self.model.sync_date, '%Y-%m-%W').label('week'),
            self.model.instrument_uid,
            func.count().label('count')
        ).filter(
            self.model.sync_date >= func.now() - text('interval 30 day'),
            self.model.synced > 0
        ).group_by(
            func.date_format(self.model.sync_date, '%Y-%m-%W'),
            self.model.instrument_uid,
        ).order_by(
            func.date_format(self.model.sync_date, '%Y-%m-%W'),
            self.model.instrument_uid,
        )

        with Session(engine) as session:
            results = session.execute(synced_hourly)
            stats["synced_hourly"] = results.all()
            results = session.execute(synced_daily)
            stats["synced_daily"] = results.all()
            results = session.execute(synced_weekly)
            stats["synced_weekly"] = results.all()
        return stats
