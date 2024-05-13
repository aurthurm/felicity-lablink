from flablink.gateway.models import Instrument


class InstrumentService:
    def __init__(self):
        ...

    def find_all(self) -> list[Instrument]:
        return Instrument.all()

    def find_one(self, uid: str) -> Instrument | None:
        return Instrument.find(uid)

    def find_one_by(self, **kwargs) -> Instrument | None:
        return Instrument.get(**kwargs)

    def create(self, **kwargs) -> Instrument:
        return Instrument.create(**kwargs)
    
    def update(self, uid: str, **kwargs) -> Instrument | None:
        inst = self.find_one(uid)
        return inst.update(**kwargs)

    def delete(self, uid: str) -> str:
        inst = self.find_one(uid)
        inst.delete()
