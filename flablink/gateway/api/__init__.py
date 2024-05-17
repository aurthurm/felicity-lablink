from fastapi import APIRouter

from .orders import (
    order_routes,
    result_exclusions_routes,
    result_translation_routes,
    keyword_mapping_routes
)
from .instruments import instrument_routes
from .settings import (
    lims_setting_routes, 
    link_setting_routes
)

api = APIRouter()
api.include_router(order_routes, prefix="/orders", tags=["Orders"])
api.include_router(result_exclusions_routes, prefix="/result-exclusions", tags=["Result Exclusions"])
api.include_router(result_translation_routes, prefix="/result-translations", tags=["Result Translations"])
api.include_router(keyword_mapping_routes, prefix="/keyword-mappings", tags=["Keyword Mappings"])
api.include_router(instrument_routes, prefix="/instruments", tags=["Instruments"])
api.include_router(lims_setting_routes, prefix="/lims-settings", tags=["Lims Settings"])
api.include_router(link_setting_routes, prefix="/link-settings", tags=["Link Settings"])
