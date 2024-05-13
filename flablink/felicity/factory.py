from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware

from flablink.config import STATIC_DIR
from flablink.gateway.seeder import seed_all
from flablink.gateway.extensions.event.register import observe_events
from flablink.gateway.api import api


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_all()
    observe_events()
    #
    yield
    #
    ...


def register_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_routes(app: FastAPI):
    @app.get("/health")
    async def get_health(request: Request):
        return {"up": True}

    app.include_router(api, prefix="/api/v1")
    
    app.mount("/assets", StaticFiles(directory=f"{STATIC_DIR}/assets"), name="assets")
    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        return Jinja2Templates(directory=STATIC_DIR).TemplateResponse("index.html", {"request": request})


def create_app(config: dict):
    config["lifespan"] = lifespan
    app = FastAPI(**config)
    register_cors(app)
    register_routes(app)
    return app
