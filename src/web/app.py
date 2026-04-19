from fastapi import FastAPI

from src.web.routers.api import router as api_router


def create_app(analysis=None) -> FastAPI:
    app = FastAPI(
        title="Medical Supplement Advisor",
        description="Interaktywny dashboard analizy badań krwi",
    )
    app.state.analysis = analysis

    # Register routers
    app.include_router(api_router)

    # Also add /health at root level for convenience
    @app.get("/health")
    async def root_health():
        return {"status": "ok"}

    return app
