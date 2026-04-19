from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from starlette.templating import Jinja2Templates
import json

router = APIRouter(tags=["Pages"])

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATES_DIR)),
    autoescape=True,
    cache_size=0,
)
templates = Jinja2Templates(env=_env)


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    analysis = request.app.state.analysis
    if analysis is None:
        return templates.TemplateResponse(
            request,
            "dashboard.html",
            {"analysis": None, "analysis_json": "null"},
        )
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "analysis": analysis,
            "analysis_json": json.dumps(
                analysis.model_dump(mode="json"), ensure_ascii=False
            ),
        },
    )
