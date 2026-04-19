from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.web.routers.api import router as api_router
from src.web.routers.pages import router as pages_router

_STATIC_DIR = Path(__file__).resolve().parent / "static"


def create_app(analysis=None) -> FastAPI:
    app = FastAPI(
        title="Medical Supplement Advisor",
        description="Interaktywny dashboard analizy badań krwi",
    )
    app.state.analysis = analysis

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)
    app.include_router(pages_router)

    if _STATIC_DIR.is_dir():
        app.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")

    @app.get("/health")
    async def root_health():
        return {"status": "ok"}

    return app
