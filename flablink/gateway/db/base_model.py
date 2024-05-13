from typing import NoReturn
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from sqlalchemy import Column, Integer
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from flablink.gateway.utils import classproperty
from flablink.gateway.db.async_mixins import AllFeaturesMixin, TimestampsMixin, smart_query
from flablink.gateway.db.session import engine


class DBModel(AllFeaturesMixin, TimestampsMixin):
    __abstract__ = True

    uid = Column(
        Integer, primary_key=True, index=True, nullable=False, autoincrement=True
    )

    @classproperty
    def settable_attributes(cls):
        return cls.columns + cls.hybrid_properties + cls.settable_relations

    def fill(self, **kwargs) -> Self:
        for name in kwargs.keys():
            if name in self.settable_attributes:
                setattr(self, name, kwargs[name])
            else:
                raise KeyError("Attribute '{}' doesn't exist".format(name))

        return self

    @classmethod
    def create(cls, **kwargs) -> Self:
        """Returns a new get instance of the class
        This is so that mutations can work well and prevent IO issues
        """
        fill = cls().fill(**kwargs)
        return cls.save(fill)

    def update(self, **kwargs) -> Self:
        """Returns a new get instance of the class
        This is so that mutations can work well and prevent IO issues
        """
        fill = self.fill(**kwargs)
        return fill.save()

    def save(self) -> Self:
        """Saves the updated model to the current entity db.
        """
        with Session(bind=engine, expire_on_commit=False) as session:
            try:
                session.add(self)
                session.flush()
                session.commit()
            except Exception:
                session.rollback()
                raise
        return self

    def delete(self) -> NoReturn:
        """Removes the model from the current entity session and mark for deletion.
        """
        with Session(engine) as session:
            session.delete(self)
            session.flush()
            session.commit()
            
    @classmethod
    def all(cls) -> list[Self] | None:
        with Session(engine) as session:
            result = session.execute(select(cls))
            _all = result.scalars().all()
        return _all

    @classmethod
    def first(cls) -> Self | None:
        with Session(engine) as session:
            result = session.execute(select(cls))
            _first = result.scalars().first()
        return _first

    @classmethod
    def find(cls, uid) -> Self | None:
        query = select(cls).where(cls.uid == uid)
        with Session(engine) as session:
            result = session.execute(query)
            found_or = result.scalars().one_or_none()
        return found_or

    @classmethod
    def find_all(cls, filters, limit=None) -> list[Self]:
        stmt = cls.smart_query(filters)
        if limit:
            stmt = stmt.limit(limit)
        with Session(engine) as session:
            results = session.execute(stmt)
            _all = results.scalars().all()
        return _all

    @classmethod
    def get(cls, **kwargs) -> Self:
        stmt = cls.where(**kwargs)
        with Session(engine) as session:
            results = session.execute(stmt)
            found = results.scalars().first()
        return found
    
    @classmethod
    def get_all(cls, limit, **kwargs) -> list[Self]:
        stmt = cls.where(**kwargs)
        if limit:
            stmt = stmt.limit(limit)
        with Session(engine) as session:
            results = session.execute(stmt)
            _all = results.scalars().all()
        return _all
