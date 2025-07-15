from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from organization_server_demo.modules.claire.routers.bots import router as bots_router
from organization_server_demo.modules.claire.routers.sessions import router as session_router
from . import __version__ as organization_server_demo_version
from .settings import SHARED_SETTINGS

app = FastAPI(title="Organization Server Demo", version=organization_server_demo_version)

if SHARED_SETTINGS.cors.allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=SHARED_SETTINGS.cors.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
@app.get("/health")
async def health():
    return {
        "name": "organization-server-demo",
        "status": "ok",
        "version": organization_server_demo_version,
    }


app.include_router(session_router, prefix="/session")
app.include_router(bots_router, prefix="/bots")
