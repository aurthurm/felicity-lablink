from typing import List
from fastapi import Depends

from sqlalchemy import or_
from flablink.gateway.api.base import BaseRouter
from flablink.gateway.services.order import (
    OrderService, ResultExclusionsService, ResultTranslationService, KeywordMappingService
)
from flablink.gateway.schemas.order import (
    OrderSchema, OrderSchemaDB,
    ResultExclusionsSchema, ResultExclusionsSchemaDB,
    ResultTranslationSchema, ResultTranslationSchemaDB,
    KeywordMappingSchema, KeywordMappingSchemaDB
)
from flablink.gateway.utils import marshaller

# Order 
order_routes = BaseRouter[OrderService, OrderSchemaDB, OrderSchema](
    OrderService, OrderSchemaDB, OrderSchema, routes=[None]
).get_routes()

@order_routes.get("", response_model=List[OrderSchemaDB])
async def all_orders(filter: str = None, service: OrderService = Depends()):
    if not filter:
        all = service.find_all(limit=1000)
    else:
        filter = f"%{filter}%"
        all = service.find_all(
            filters={
                or_: {
                    "test_id__like": filter,
                    "keyword__like": filter,
                    "instrument__like": filter,
                    "result__like": filter,
                    "result_date__like": filter,
                    "result__like": filter,
                    "synced__like": filter,
                    "synced__like": filter,
                    "sync_date__like": filter
                }
            },
            limit=1000
        )
    return [OrderSchemaDB(**marshaller(inst)) for inst in all]

@order_routes.post("/resync/{uid}", response_model=OrderSchema)
async def api_orders(uid, order_service: OrderService = Depends()):
    return order_service.update(uid, syned=0)

@order_routes.get("/stats")
async def order_stats(order_service: OrderService = Depends()):
    return order_service.statistics()

# ResultExclusions
result_exclusions_routes = BaseRouter[ResultExclusionsService, ResultExclusionsSchemaDB, ResultExclusionsSchema](
    ResultExclusionsService, ResultExclusionsSchemaDB, ResultExclusionsSchema
).get_routes()


# ResultTranslation
result_translation_routes = BaseRouter[ResultTranslationService, ResultTranslationSchemaDB, ResultTranslationSchema](
    ResultTranslationService, ResultTranslationSchemaDB, ResultTranslationSchema
).get_routes()

# KeywordMapping
keyword_mapping_routes = BaseRouter[KeywordMappingService, KeywordMappingSchemaDB, KeywordMappingSchema](
    KeywordMappingService, KeywordMappingSchemaDB, KeywordMappingSchema
).get_routes()