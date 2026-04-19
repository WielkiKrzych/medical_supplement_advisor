from fastapi import FastAPI


def create_app(analysis=None) -> FastAPI:
    app = FastAPI(
        title="Medical Supplement Advisor",
        description="Interaktywny dashboard analizy badań krwi",
    )
    app.state.analysis = analysis
    return app
