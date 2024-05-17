from flablink.gateway.api.base import BaseRouter
from flablink.gateway.services.settings import (
    LimsSettingsService, LinkSettingsService
)
from flablink.gateway.schemas.settings import (
    LimsSettingsSchema, LimsSettingsSchemaDB,
    LinkSettingsSchema, LinkSettingsSchemaDB,
)

# LimsSettings 
lims_setting_routes = BaseRouter[LimsSettingsService, LimsSettingsSchemaDB, LimsSettingsSchema](
    LimsSettingsService, LimsSettingsSchemaDB, LimsSettingsSchema,
    routes=["all", "update"]
).get_routes()


# LinkSettings 
link_setting_routes = BaseRouter[LinkSettingsService, LinkSettingsSchemaDB, LinkSettingsSchema](
    LinkSettingsService, LinkSettingsSchemaDB, LinkSettingsSchema,
    routes=["all", "update"]
).get_routes()