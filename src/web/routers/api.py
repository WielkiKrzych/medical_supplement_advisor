from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["API"])


@router.get("/health")
async def health_check():
    return {"status": "ok"}
