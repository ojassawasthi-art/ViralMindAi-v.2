"""AI Branding Agency & Creative Design Studio Engine."""

from __future__ import annotations

from typing import Any, Dict, List

from backend.schemas import BrandBuildRequest, DesignBriefRequest


PALETTE_LIBRARY: Dict[str, Dict[str, Any]] = {
    "value": {
        "name": "Accessible Energy",
        "primary": "#0F766E",
        "secondary": "#F59E0B",
        "background": "#F8FAFC",
        "ink": "#0F172A",
        "psychology": "Teal signals reliability and clarity; warm amber drives approachable action without luxury intimidation.",
    },
    "mid_premium": {
        "name": "Editorial Authority",
        "primary": "#111827",
        "secondary": "#6366F1",
        "accent": "#10B981",
        "background": "#F9FAFB",
        "ink": "#111827",
        "psychology": "Deep charcoal establishes editorial credibility; indigo communicates modern intelligence; emerald reinforces measurable growth.",
    },
    "luxury": {
        "name": "Quiet Precision",
        "primary": "#09090B",
        "secondary": "#D4AF37",
        "background": "#FAF7F2",
        "ink": "#18181B",
        "psychology": "Obsidian and warm alabaster create generous negative space; muted gold signals heritage craft and selectivity.",
    },
}

PLATFORM_DIMENSIONS: Dict[str, str] = {
    "instagram_reels": "1080 x 1920 px (9:16 vertical; keep key text inside central 1080 x 1420 safe zone)",
    "instagram_carousel": "1080 x 1350 px (4:5 portrait for maximum mobile feed real estate)",
    "youtube_thumbnail": "1280 x 720 px (16:9; readable at 168 x 94 px mobile preview)",
    "linkedin": "1200 x 1350 px (4:5 document/image) or 1200 x 627 px (link card)",
    "x": "1600 x 900 px (16:9) or 1200 x 1200 px (1:1)",
    "landing_page": "1440 px desktop container / 390 px mobile-first responsive grid",
}


def build_brand_identity(req: BrandBuildRequest) -> Dict[str, Any]:
    palette = PALETTE_LIBRARY.get(req.price_positioning, PALETTE_LIBRARY["mid_premium"])
    clean_topic = req.business_or_idea.strip()
    slug = "".join(ch for ch in clean_topic.title() if ch.isalnum())[:12] or "Brand"

    name_concepts = [
        {"name": f"{slug}Lab", "rationale": "Signals research-backed precision and modern experimentation."},
        {"name": f"North{slug}", "rationale": "Evokes clear direction, reliability, and category leadership."},
        {"name": f"Craft{slug}", "rationale": "Emphasizes human quality and intentional execution."},
    ]

    return {
        "brand_seed": clean_topic,
        "niche": req.niche,
        "target_audience": req.target_audience,
        "positioning_strategy": {
            "unique_selling_proposition": (
                f"Unlike generic {req.niche} alternatives, {clean_topic} combines evidence-based transparency "
                f"with practical execution built specifically for {req.target_audience}."
            ),
            "competitors_analyzed": req.competitors or ["Category incumbents relying on jargon and opaque pricing"],
            "market_gap": "Audiences distrust exaggerated claims and crave clear, proof-driven guidance.",
            "brand_personality": ["Clear", "Evidence-led", "Respectful", "Sharp"],
            "brand_voice": f"Direct, jargon-free, grounded in {', '.join(req.values)}.",
        },
        "naming_concepts": name_concepts,
        "mission_and_vision": {
            "mission": f"Equip {req.target_audience} with transparent, high-craft {req.niche} solutions.",
            "vision": f"Become the most trusted benchmark for measurable quality in {req.niche}.",
        },
        "visual_system": {
            "color_palette": palette,
            "typography": {
                "display": "Space Grotesk or Instrument Serif (editorial authority)",
                "body": "Inter or Plus Jakarta Sans (high legibility on mobile)",
                "mono": "JetBrains Mono (metrics, badges, and data callouts)",
            },
            "logo_direction": "Geometric wordmark + minimal monogram mark legible at 24x24px favicon size.",
        },
        "channel_direction": {
            "social_media_identity": "Consistent 2-color thumbnail/carousel header system with 3-word hook banners.",
            "website_direction": "Lead with concrete outcome proof above the fold, interactive demo/calculator, and transparent pricing.",
            "packaging_or_onboarding": "Include a 1-page quick-start card that delivers an immediate 'first win' in under 5 minutes.",
        },
    }


def generate_design_brief(req: DesignBriefRequest) -> Dict[str, Any]:
    dimensions = PLATFORM_DIMENSIONS.get(req.platform.lower(), "1080 x 1350 px (4:5) or 1920 x 1080 px (16:9)")
    msg = req.key_message.strip() or f"{req.brand_name}: {req.topic}"

    return {
        "asset_type": req.asset_type,
        "brand_name": req.brand_name,
        "platform": req.platform,
        "dimensions": dimensions,
        "layout_and_composition": {
            "grid": "12-column responsive grid with generous 8–12% outer margin.",
            "focal_point": "Single dominant visual subject or metric occupying 45–55% of frame.",
            "text_placement": "Top-left or upper-third headline (max 5–7 words), bottom-left subtle brand mark.",
        },
        "visual_hierarchy": [
            f"1. Primary Hook Text: '{msg}' (largest weight, >= 4.5:1 WCAG contrast)",
            "2. Visual Proof Element: Product/interface/subject with directional lighting",
            "3. Supporting Micro-Copy / Badge: 1 concise proof point or CTA",
        ],
        "color_psychology": f"Mood '{req.color_mood}': pair a deep neutral canvas with 1 high-contrast focal accent so the eye lands on the hook within 0.5 seconds.",
        "typography_direction": "Bold geometric sans-serif for headline (-0.02em tracking), clean regular sans for subtext.",
        "image_generation_prompt": (
            f"Editorial commercial {req.asset_type} visual for {req.brand_name} about {req.topic}, "
            f"{req.color_mood} lighting, clean negative space on upper third for typography, "
            "sharp studio photography, no cluttered text artifacts."
        ),
    }
