from fastapi import Depends

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

# Order 
order_routes = BaseRouter[OrderService, OrderSchemaDB, OrderSchema](
    OrderService, OrderSchemaDB, OrderSchema
).get_routes()

@order_routes.post("/resync/{uid}", response_model=OrderSchema)
async def api_orders(uid, order_service: OrderService = Depends()):
    return order_service.update(uid, syned=0)


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