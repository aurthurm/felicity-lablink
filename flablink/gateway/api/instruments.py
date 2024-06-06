from fastapi import Depends
from flablink.gateway.api.base import BaseRouter
from flablink.gateway.services.connection import ConnectionService
from flablink.gateway.services.instrument import (
    InstrumentService
)
from flablink.gateway.schemas.instrument import (
    InstrumentSchema, InstrumentSchemaDB, InstrumentConnection
)

# Instrument 
instrument_routes = BaseRouter[InstrumentService, InstrumentSchemaDB, InstrumentSchema](
    InstrumentService, InstrumentSchemaDB, InstrumentSchema
).get_routes()

@instrument_routes.post("/connect")
async def instrument_connection(data: InstrumentConnection, connection_service: ConnectionService = Depends()):
    match data.action:
        case "connect":
            connection_service.connect(data.uid)
        case "disconnect":
            connection_service.disconnect(data.uid)
        case _:
            raise ValueError("Invalid action")
    return {"status": "success"}
