"""AI Content Generation Studio turning one idea into complete multi-platform campaigns."""

from __future__ import annotations

from typing import Any, Dict, List

from backend.schemas import ContentCampaignRequest


CONTENT_ARCHETYPES = [
    ("Contrarian Myth-Buster", "Curiosity Gap + Pattern Interrupt", "instagram_reels"),
    ("Step-by-Step Screen/Demo Teardown", "Utility + Saveability", "youtube_shorts"),
    ("Before vs. After Case Study", "Social Proof + Transformation", "tiktok"),
    ("5-Slide Actionable Checklist Carousel", "High Save Rate + Clarity", "instagram_carousel"),
    ("Founder Mistake & Lesson Story", "Relatability + Trust", "linkedin"),
    ("Data-Backed Breakdown Thread", "Authority + Bookmarks", "x_thread"),
    ("Buyer Objection Comparison", "Purchase Intent + Search", "youtube_long_form"),
    ("Behind-the-Scenes Craft Process", "Authenticity + Retention", "instagram_reels"),
    ("SEO Problem-Solution Pillar Guide", "Evergreen Search Capture", "seo_article"),
    ("3-Email Welcome & Proof Sequence", "Conversion + Retention", "email_campaign"),
]


def generate_content_campaign(req: ContentCampaignRequest) -> Dict[str, Any]:
    ideas: List[Dict[str, Any]] = []
    count = max(1, min(100, req.idea_count))

    for idx in range(count):
        arch_name, psych_driver, default_plat = CONTENT_ARCHETYPES[idx % len(CONTENT_ARCHETYPES)]
        plat = req.platforms[idx % len(req.platforms)] if req.platforms else default_plat
        angle_num = idx + 1

        ideas.append(
            {
                "id": angle_num,
                "archetype": arch_name,
                "concept": f"[{arch_name} #{angle_num}] Apply '{req.idea}' to solve a concrete {req.niche} bottleneck for {req.target_audience}.",
                "target_audience": req.target_audience,
                "hook": f"Stop guessing {req.niche}: here is the {arch_name.lower()} behind '{req.idea}' (#{angle_num}).",
                "script_or_structure": [
                    "0–3s (Hook): State the surprising outcome or common mistake directly on camera/text.",
                    "3–15s (Context & Proof): Show the exact before/after or 3-step workflow on screen.",
                    "15–35s (Payoff): Deliver the actionable takeaway and one counter-intuitive nuance.",
                    "35–45s (CTA): Prompt viewers to save/comment a keyword for the checklist.",
                ],
                "visual_direction": f"High-contrast framing in {req.tone} style; show real product/workflow proof in the first 2 seconds.",
                "editing_instructions": "Cut dead air every 2–3 seconds; use bold readable captions inside 9:16 safe zones; add subtle sound rise at the reveal.",
                "caption": f"Most {req.target_audience} overlook this part of {req.idea}. Save this breakdown so you can test it this week. ({req.language})",
                "cta": "Save this post for your next sprint and comment 'CHECKLIST' if you want the template.",
                "hashtag_and_keyword_strategy": {
                    "primary_keywords": [req.niche.lower(), req.idea.lower()[:40], req.target_audience.lower()[:30]],
                    "hashtags": [
                        f"#{req.niche.replace(' ', '')}",
                        "#MarketingStrategy",
                        "#GrowthPlaybook",
                    ],
                },
                "platform_recommendation": plat,
                "reasoning_behind_potential": f"Leverages {psych_driver} tailored to {req.target_audience} on {plat}.",
                "performance_measurement_plan": {
                    "primary_kpis": ["3-second hold rate", "Average watch %", "Saves per reach", "Shares per reach"],
                    "experiment_note": "Log actual views, watch %, shares, and saves in Campaign Analytics after 72 hours.",
                },
            }
        )

    calendar_7_day = [
        {"day": f"Day {d}", "platform": ideas[(d - 1) % len(ideas)]["platform_recommendation"], "focus": ideas[(d - 1) % len(ideas)]["archetype"]}
        for d in range(1, 8)
    ]

    return {
        "campaign_seed": req.idea,
        "niche": req.niche,
        "target_audience": req.target_audience,
        "tone": req.tone,
        "language": req.language,
        "total_ideas_generated": len(ideas),
        "ideas": ideas,
        "weekly_content_calendar": calendar_7_day,
    }
