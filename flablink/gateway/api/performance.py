from flablink.gateway.api.base import BaseRouter
from flablink.gateway.services.performance import (
    ForwarderService, ForwarderPerfService
)
from flablink.gateway.schemas.performance import (
    ForwarderSchema, ForwarderSchemaDB,
    ForwarderPerfSchema, ForwarderPerfSchemaDB,
)

# Forwarder 
forwarder_routes = BaseRouter[ForwarderService, ForwarderSchemaDB, ForwarderSchema](
    ForwarderService, ForwarderSchemaDB, ForwarderSchema,
    routes=["all"]
).get_routes()


# ForwarderPerf 
forwarder_perf_routes = BaseRouter[ForwarderPerfService, ForwarderPerfSchemaDB, ForwarderPerfSchema](
    ForwarderPerfService, ForwarderPerfSchemaDB, ForwarderPerfSchema,
    routes=["all"]
).get_routes()