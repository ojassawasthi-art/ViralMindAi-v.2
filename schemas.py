"""Pydantic schemas for VIRALMIND AI inputs and structured outputs."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class OnboardingRequest(BaseModel):
    goal: str = Field(..., description="What are you trying to grow?")
    niche: str = Field(..., description="Industry, category, or topic")
    target_audience: str = Field(..., description="Primary audience description")
    platforms: List[str] = Field(default_factory=lambda: ["instagram_reels", "youtube_shorts"])
    stage: str = Field(default="early", description="idea | early | scaling | established")
    tone: str = Field(default="authoritative_relatable")
    budget_tier: str = Field(default="bootstrap", description="bootstrap | growth | enterprise")


class ViralityScoreRequest(BaseModel):
    title_or_hook: str
    concept: str
    platform: str = "instagram_reels"
    target_audience: str = "general"
    niche: str = "general"
    format_type: str = "short_video"
    timing_context: str = "evergreen"
    visual_plan: str = ""
    cta: str = ""


class DimensionScore(BaseModel):
    dimension: str
    score: float = Field(..., ge=0, le=100)
    weight: float
    rationale: str


class ViralityScoreResponse(BaseModel):
    viral_potential_score: float = Field(..., ge=0, le=100)
    confidence_level: str
    calibration_note: str
    dimension_scores: List[DimensionScore]
    biggest_strengths: List[str]
    biggest_weaknesses: List[str]
    improvements_required: List[str]
    alternative_versions: List[Dict[str, str]]
    recommended_platform: str
    methodology_disclaimer: str


class TrendResearchRequest(BaseModel):
    query: str
    niche: str = "general"
    audience: str = "general"
    platforms: List[str] = Field(default_factory=lambda: ["tiktok", "instagram_reels", "youtube_shorts"])
    include_live_web: bool = False


class ContentCampaignRequest(BaseModel):
    idea: str
    niche: str
    target_audience: str
    tone: str = "bold_educational"
    language: str = "English"
    platforms: List[str] = Field(default_factory=lambda: ["instagram_reels", "youtube_shorts", "linkedin"])
    idea_count: int = Field(default=10, ge=1, le=100)


class BrandBuildRequest(BaseModel):
    business_or_idea: str
    niche: str
    target_audience: str
    values: List[str] = Field(default_factory=lambda: ["clarity", "trust", "craft"])
    competitors: List[str] = Field(default_factory=list)
    price_positioning: str = Field(default="mid_premium", description="value | mid_premium | luxury")


class DesignBriefRequest(BaseModel):
    asset_type: str = Field(..., description="logo | poster | thumbnail | carousel | ad_creative | landing_page")
    brand_name: str
    topic: str
    platform: str = "instagram_reels"
    color_mood: str = "high_contrast_editorial"
    key_message: str = ""


class PsychologyRequest(BaseModel):
    product_or_offer: str
    target_audience: str
    price_point: str = "mid"
    main_objection: str = "trust_and_roi"
    generations: List[str] = Field(default_factory=lambda: ["gen_z", "millennials"])


class GrowthRoadmapRequest(BaseModel):
    business_name: str
    niche: str
    target_audience: str
    current_baseline: str = "0-1k followers"
    primary_goal: str = "leads_and_audience"
    budget_tier: str = "bootstrap"
    platforms: List[str] = Field(default_factory=lambda: ["instagram_reels", "youtube_shorts", "seo"])


class CampaignOutcomeRequest(BaseModel):
    campaign_name: str
    platform: str
    content_format: str
    hook_used: str
    predicted_score: float = Field(..., ge=0, le=100)
    views: int = Field(default=0, ge=0)
    likes: int = Field(default=0, ge=0)
    comments: int = Field(default=0, ge=0)
    shares: int = Field(default=0, ge=0)
    saves: int = Field(default=0, ge=0)
    avg_watch_pct: float = Field(default=0.0, ge=0, le=100)
    conversions: int = Field(default=0, ge=0)
    audience_feedback: str = ""
    what_worked: str = ""
    what_failed: str = ""


class ProviderConfigUpdate(BaseModel):
    default_provider: Optional[str] = None
    fallback_providers: Optional[List[str]] = None
