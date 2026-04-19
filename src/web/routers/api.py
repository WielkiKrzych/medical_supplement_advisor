from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api", tags=["API"])


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/analysis")
async def get_analysis(request: Request):
    analysis = request.app.state.analysis
    if analysis is None:
        return JSONResponse(
            status_code=404,
            content={"error": "no_analysis", "detail": "No analysis data available"},
        )
    return analysis.model_dump(mode="json")
