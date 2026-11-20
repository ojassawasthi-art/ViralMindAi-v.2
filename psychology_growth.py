"""Ethical Consumer Psychology, Generational Fusion & Growth Strategy Engine."""

from __future__ import annotations

from typing import Any, Dict, List

from backend.schemas import GrowthRoadmapRequest, OnboardingRequest, PsychologyRequest


GENERATIONAL_PROFILES: Dict[str, Dict[str, Any]] = {
    "gen_z": {
        "habits": "Short-form vertical video, social search (TikTok/Instagram/YouTube), community-first validation.",
        "trust_signals": "Unfiltered creator demos, peer comments, transparent pricing, humor without corporate stiffness.",
        "friction_points": "Overly polished ad speak, hidden fees, slow or gated onboarding.",
    },
    "millennials": {
        "habits": "YouTube deep-dives, Instagram carousels, LinkedIn, newsletters, comparison reviews.",
        "trust_signals": "ROI clarity, time-saving workflows, credible third-party reviews, ethical brand values.",
        "friction_points": "Vague hype without proof, cluttered UX, subscription lock-in.",
    },
    "gen_alpha": {
        "habits": "Visual-first interactive platforms, YouTube Shorts, gaming/creator ecosystems (age-appropriate).",
        "trust_signals": "Playful clarity, creator-led storytelling, instant visual feedback.",
        "friction_points": "Text-heavy walls and passive static ads.",
    },
    "gen_x": {
        "habits": "YouTube tutorials, Facebook/LinkedIn, email newsletters, search engines.",
        "trust_signals": "Reliability, clear customer support, straightforward value propositions, durability.",
        "friction_points": "Gimmicky slang, forced trends, unclear next steps.",
    },
}


def analyze_consumer_psychology(req: PsychologyRequest) -> Dict[str, Any]:
    gen_insights = {
        g: GENERATIONAL_PROFILES[g]
        for g in req.generations
        if g in GENERATIONAL_PROFILES
    }
    if not gen_insights:
        gen_insights = {"millennials": GENERATIONAL_PROFILES["millennials"]}

    return {
        "offer": req.product_or_offer,
        "target_audience": req.target_audience,
        "ethical_guardrail": (
            "All recommendations apply behavioral science ethically: zero fake scarcity, "
            "zero fabricated reviews, and zero manipulative dark patterns."
        ),
        "generational_fusion_strategy": {
            "segments": gen_insights,
            "unified_bridge": (
                "Keep the core brand promise anchored in verifiable proof (appeals to Millennials/Gen X) "
                "while delivering it through fast, visual, conversational storytelling (appeals to Gen Z)."
            ),
        },
        "behavioral_levers": [
            {
                "principle": "Cognitive Fluency & Clarity",
                "application": f"State the exact outcome of '{req.product_or_offer}' in 1 sentence under 12 words to reduce mental friction.",
            },
            {
                "principle": "Verifiable Social Proof",
                "application": "Show real user screenshots, specific metrics, or transparent case studies rather than vague testimonials.",
            },
            {
                "principle": "Loss Aversion (Ethical Framing)",
                "application": f"Quantify the real time or budget wasted by the status quo before introducing '{req.product_or_offer}'.",
            },
            {
                "principle": "Objection Pre-emption",
                "application": f"Address '{req.main_objection}' directly in the FAQ, pinned comment, or 2nd slide of your carousel.",
            },
        ],
        "pricing_psychology": (
            f"For '{req.price_point}' positioning, anchor value against the cost of inaction or manual alternatives, "
            "and offer a clear entry tier or risk-free trial."
        ),
    }


def build_growth_roadmap(req: GrowthRoadmapRequest) -> Dict[str, Any]:
    return {
        "business_name": req.business_name,
        "niche": req.niche,
        "target_audience": req.target_audience,
        "baseline": req.current_baseline,
        "primary_goal": req.primary_goal,
        "budget_tier": req.budget_tier,
        "growth_forecast_note": (
            "Targets below are operational experiment milestones, not guaranteed viral outcomes. "
            "Adjust weekly based on logged retention, share rate, and conversion data."
        ),
        "sprint_7_day": [
            "Day 1–2: Audit 10 top-performing niche posts & 20 audience complaints; lock 3 content pillars.",
            "Day 3–4: Produce 5 hook variations and 3 flagship pieces (Reels/Shorts + Carousel).",
            "Day 5–6: Publish first 3 pieces, reply to every comment within 60 minutes, track 3s hold & save rate.",
            "Day 7: Log outcomes in ViralMind Campaign Analytics and double down on the top-retaining hook.",
        ],
        "plan_30_day": {
            "cadence": "4–5 native posts/week across " + ", ".join(req.platforms),
            "distribution": "Pair organic short-form discovery with 1 weekly deep-dive asset + lead magnet.",
            "experiments": "Run 4 structured A/B hook tests and 2 CTA variations.",
        },
        "roadmap_90_day": {
            "month_1": "Message-market fit: test 12+ hooks to identify top 2 repeatable formats.",
            "month_2": "Systematize winning formats, launch SEO/long-form pillar + email capture loop.",
            "month_3": "Scale distribution via creator collaborations, retargeting top-performing organic posts, and conversion optimization.",
        },
        "kpi_scorecard": [
            "Reach & Non-Follower Impressions",
            "3-Second Hold Rate & Average Watch %",
            "Saves + Shares per 1,000 Views",
            "Profile/Link CTR & Lead Conversion Rate",
        ],
    }


def run_guided_onboarding(req: OnboardingRequest) -> Dict[str, Any]:
    """Entry point for 'What are you trying to grow?' workflow."""
    return {
        "intake_summary": {
            "goal": req.goal,
            "niche": req.niche,
            "target_audience": req.target_audience,
            "platforms": req.platforms,
            "stage": req.stage,
        },
        "recommended_sequence": [
            {
                "step": 1,
                "module": "Trend & Competitor Radar",
                "action": f"Research active demand and audience complaints in '{req.niche}' before writing.",
            },
            {
                "step": 2,
                "module": "Consumer Psychology & Brand Positioning",
                "action": f"Define why '{req.target_audience}' should trust and remember you.",
            },
            {
                "step": 3,
                "module": "Content Studio + Virality Scorer",
                "action": f"Generate 10+ native concepts for {', '.join(req.platforms)} and score hooks before filming.",
            },
            {
                "step": 4,
                "module": "7-Day Growth Sprint & Analytics Loop",
                "action": "Ship 3 tests this week and log actual metrics to calibrate future predictions.",
            },
        ],
    }
