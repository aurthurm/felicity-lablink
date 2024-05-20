from typing import TypeVar, Generic, List

from pydantic import BaseModel
from fastapi import APIRouter, Depends

from flablink.gateway.services.base import BaseService
from flablink.gateway.utils import marshaller

Service = TypeVar("Service", bound=BaseService)
Schema = TypeVar("Schema", bound=BaseModel)
SchemaIn = TypeVar("SchemaIn", bound=BaseModel)


class BaseRouter(Generic[Service, Schema, SchemaIn]):
    def __init__(self, service: Service, schema: Schema, schema_in: SchemaIn, routes: List[str] = None):
        self.service = service
        self.Schema = schema
        self.SchemaIn = schema_in
        self.router = APIRouter()
        self.routes = routes

        if not self.routes or "all" in self.routes:
            @self.router.get("", response_model=List[self.Schema])
            async def get_all(filter: str = None, service: self.service = Depends()):
                print(f"filter -> {filter}")
                all = service.find_all()
                return [self.Schema(**marshaller(inst)) for inst in all]

        if not self.routes or "one" in self.routes:
            @self.router.get("/{uid}", response_model=self.Schema)
            async def get_one(uid: str, service: self.service = Depends()):
                one = service.find_one(uid)
                return self.Schema(**marshaller(one)) if one else None
            
        if not self.routes or "create" in self.routes:
            @self.router.post("/", response_model=self.Schema)
            async def create(data: self.SchemaIn, service: self.service = Depends()):
                created = service.create(**data.dict())
                return self.Schema(**marshaller(created))
            
        if not self.routes or "update" in self.routes:
            @self.router.put("/{uid}", response_model=self.Schema)
            async def update(uid: str, data: self.SchemaIn, service: self.service = Depends()):
                updated = service.update(uid, **data.dict())
                return self.Schema(**marshaller(updated))
            
        if not self.routes or "delete" in self.routes:
            @self.router.delete("/{uid}", response_model=str)
            async def delete(uid: str, service: self.service = Depends()):
                service.delete(uid)
                return uid

    def get_routes(self):
        return self.router
