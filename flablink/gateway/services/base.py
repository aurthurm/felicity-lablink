from typing import Generic, TypeVar
from flablink.gateway.db.base_model import DBModel

M = TypeVar("M", bound=DBModel)


class BaseService(Generic[M]):
    def __init__(self, model: M):
        self.model = model

    def find_all(self) -> list[M]:
        return self.model.all()

    def find_one(self, uid: int) -> M | None:
        return self.model.find(uid)

    def find_one_by(self, **kwargs) -> M | None:
        return self.model.get(**kwargs)

    def create(self, **kwargs) -> M:
        return self.model.create(**kwargs)
    
    def update(self, uid: int, **kwargs) -> M | None:
        inst = self.find_one(uid)
        return inst.update(**kwargs)

    def delete(self, uid: int) -> int:
        inst = self.find_one(uid)
        inst.delete()
