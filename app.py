"""FastAPI REST API & Dashboard Server for VIRALMIND AI."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.config import BASE_DIR, settings
from backend.engines.branding_agency import build_brand_identity, generate_design_brief
from backend.engines.content_studio import generate_content_campaign
from backend.engines.platform_intelligence import analyze_platform, list_supported_platforms
from backend.engines.psychology_growth import (
    analyze_consumer_psychology,
    build_growth_roadmap,
    run_guided_onboarding,
)
from backend.engines.trend_research import research_trends
from backend.engines.viral_scoring import score_virality
from backend.schemas import (
    BrandBuildRequest,
    CampaignOutcomeRequest,
    ContentCampaignRequest,
    DesignBriefRequest,
    GrowthRoadmapRequest,
    OnboardingRequest,
    ProviderConfigUpdate,
    PsychologyRequest,
    TrendResearchRequest,
    ViralityScoreRequest,
)
from database.store import learning_store
from server.providers.router import router as provider_router


app = FastAPI(
    title="VIRALMIND AI",
    description="AI-powered marketing intelligence, branding, creative direction & viral growth agency platform.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_token(authorization: Optional[str] = Header(default=None)) -> None:
    """Enforce Bearer token auth if VIRALMIND_API_TOKEN is configured."""
    expected = settings.api_token.strip()
    if not expected:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = authorization.removeprefix("Bearer ").strip()
    if token != expected:
        raise HTTPException(status_code=403, detail="Invalid API token")


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "viralmind-ai",
        "version": "1.0.0",
        "default_provider": provider_router.default_provider,
    }


@app.post("/api/v1/onboarding", dependencies=[Depends(verify_token)])
def api_onboarding(req: OnboardingRequest) -> dict:
    brief = run_guided_onboarding(req)
    project_id = learning_store.save_project(
        goal=req.goal,
        niche=req.niche,
        target_audience=req.target_audience,
        platforms=req.platforms,
        stage=req.stage,
        brief=brief,
    )
    return {"project_id": project_id, **brief}


@app.get("/api/v1/projects", dependencies=[Depends(verify_token)])
def api_list_projects(limit: int = Query(default=20, ge=1, le=100)) -> dict:
    return {"projects": learning_store.list_projects(limit=limit)}


@app.post("/api/v1/virality/score", dependencies=[Depends(verify_token)])
def api_score_virality(req: ViralityScoreRequest) -> dict:
    return score_virality(req).model_dump()


@app.get("/api/v1/platforms", dependencies=[Depends(verify_token)])
def api_list_platforms() -> dict:
    return {"platforms": list_supported_platforms()}


@app.get("/api/v1/platforms/{platform}", dependencies=[Depends(verify_token)])
def api_analyze_platform(platform: str) -> dict:
    return analyze_platform(platform)


@app.post("/api/v1/trends/research", dependencies=[Depends(verify_token)])
def api_research_trends(req: TrendResearchRequest) -> dict:
    return research_trends(req)


@app.post("/api/v1/content/generate", dependencies=[Depends(verify_token)])
def api_generate_content(req: ContentCampaignRequest) -> dict:
    return generate_content_campaign(req)


@app.post("/api/v1/brand/build", dependencies=[Depends(verify_token)])
def api_build_brand(req: BrandBuildRequest) -> dict:
    return build_brand_identity(req)


@app.post("/api/v1/design/brief", dependencies=[Depends(verify_token)])
def api_design_brief(req: DesignBriefRequest) -> dict:
    return generate_design_brief(req)


@app.post("/api/v1/psychology/analyze", dependencies=[Depends(verify_token)])
def api_analyze_psychology(req: PsychologyRequest) -> dict:
    return analyze_consumer_psychology(req)


@app.post("/api/v1/growth/roadmap", dependencies=[Depends(verify_token)])
def api_growth_roadmap(req: GrowthRoadmapRequest) -> dict:
    return build_growth_roadmap(req)


@app.post("/api/v1/analytics/outcomes", dependencies=[Depends(verify_token)])
def api_log_outcome(req: CampaignOutcomeRequest) -> dict:
    return learning_store.log_outcome(req.model_dump())


@app.get("/api/v1/analytics/insights", dependencies=[Depends(verify_token)])
def api_get_insights(query: str = "", platform: str = "") -> dict:
    return learning_store.search_experiments(query=query, platform=platform)


@app.get("/api/v1/providers/status", dependencies=[Depends(verify_token)])
def api_provider_status() -> dict:
    return provider_router.status()


@app.post("/api/v1/providers/configure", dependencies=[Depends(verify_token)])
def api_provider_configure(req: ProviderConfigUpdate) -> dict:
    return provider_router.configure(
        default_provider=req.default_provider,
        fallback_providers=req.fallback_providers,
    )


FRONTEND_DIR: Path = BASE_DIR / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/", include_in_schema=False)
    def serve_dashboard() -> FileResponse:
        return FileResponse(str(FRONTEND_DIR / "index.html"))
