from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from flablink.config import STATIC_DIR, SEED_LABLINK
from flablink.gateway.extensions.event.register import observe_events
from flablink.gateway.api import api
from flablink.gateway.logger import Logger
from flablink.gateway.tasks import start_scheduler, shutdown_scheduler
from flablink.gateway.extensions.channel.channel import broadcast
from flablink.gateway.extensions.channel.base import Channels

logger = Logger(__name__, __file__)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     observe_events()
#     init_bg_scheduler()
#     yield
#     ...

def register_app_events(app: FastAPI): 
    @app.on_event("startup")
    def startup_event():
        logger.log("info", "Server starting up............................................")
        observe_events()  
        start_scheduler()

    @app.on_event("shutdown")
    def shutdown_event():
        logger.log("info", "Server shutting down............................................")
        shutdown_scheduler()


def register_cors(app: FastAPI):
    origins = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_routes(app: FastAPI):

    @app.get("/health", tags=["Health"], response_model=dict)
    async def get_health(request: Request):
        return {"up": True}

    app.include_router(api, prefix="/api/v1")
    
    app.mount("/assets", StaticFiles(directory=f"{STATIC_DIR}/assets"), name="assets")
    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def home(request: Request):
        return Jinja2Templates(directory=STATIC_DIR).TemplateResponse("index.html", {"request": request})


def register_websocket(app: FastAPI):
    @app.websocket("/ws/{client_id}")
    async def websocket_endpoint(websocket: WebSocket, client_id):
        await websocket.accept()
        async with broadcast.subscribe(channel=Channels.ACTIVITIES) as subscriber:
            while True:  # Continuously listen for broadcast messages
                event = await subscriber.get()
                try:
                    await websocket.send_json(event.message)
                except Exception as e:
                    ...


def create_app():
    config = dict()
    config["title"] = "Felicity LabLink"
    config["description"] = "Serial and Socket Communication Gateway"
    # config["lifespan"] = lifespan
    
    app = FastAPI(**config)
    register_cors(app)
    register_routes(app)
    register_app_events(app)
    register_websocket(app)
    return app
