from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json

router = APIRouter(tags=["Pages"])
templates = Jinja2Templates(directory="src/web/templates")


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    analysis = request.app.state.analysis
    if analysis is None:
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "analysis": None,
                "analysis_json": "null",
            },
        )
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "analysis": analysis,
            "analysis_json": json.dumps(
                analysis.model_dump(mode="json"), ensure_ascii=False
            ),
        },
    )
