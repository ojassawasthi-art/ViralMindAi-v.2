"""Proprietary 11-dimension Viral Potential Scoring Engine (0-100)."""

from __future__ import annotations

import re
from typing import Dict, List

from backend.schemas import DimensionScore, ViralityScoreRequest, ViralityScoreResponse
from database.store import learning_store


DIMENSION_WEIGHTS: Dict[str, float] = {
    "hook_strength": 0.16,
    "emotional_impact": 0.11,
    "audience_relevance": 0.12,
    "novelty": 0.09,
    "shareability": 0.12,
    "retention_potential": 0.12,
    "visual_appeal": 0.08,
    "timing": 0.05,
    "trend_relevance": 0.05,
    "competition": 0.05,
    "platform_compatibility": 0.05,
}

CURIOSITY_TRIGGERS = ("why", "how", "stop", "mistake", "secret", "truth", "never", "nobody", "what if", "tested")
EMOTIONAL_TRIGGERS = ("afraid", "love", "hate", "shocking", "finally", "regret", "proud", "save", "risk", "transform")
SHARE_TRIGGERS = ("share", "send this", "tag", "checklist", "framework", "template", "myth", "comparison", "vs")


def _clamp(val: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return round(max(lo, min(hi, val)), 1)


def score_virality(req: ViralityScoreRequest) -> ViralityScoreResponse:
    hook = req.title_or_hook.strip()
    hook_lower = hook.lower()
    concept_lower = req.concept.lower()
    combined = f"{hook_lower} {concept_lower}"

    # 1. Hook strength (conciseness, specificity, curiosity gap, numbers)
    word_count = len(hook.split())
    hook_score = 52.0
    if 4 <= word_count <= 14:
        hook_score += 18.0
    elif word_count > 18:
        hook_score -= 8.0
    if any(t in hook_lower for t in CURIOSITY_TRIGGERS):
        hook_score += 14.0
    if re.search(r"\d+", hook):
        hook_score += 10.0
    if "?" in hook:
        hook_score += 5.0

    # 2. Emotional impact
    emo_hits = sum(1 for t in EMOTIONAL_TRIGGERS if t in combined)
    emo_score = 48.0 + min(38.0, emo_hits * 12.0) + (8.0 if "!" not in hook else 2.0)

    # 3. Audience relevance
    aud_specific = len(req.target_audience.strip()) > 10 and req.target_audience.lower() != "general"
    aud_score = 78.0 if aud_specific else 46.0
    if req.niche.lower() in combined:
        aud_score += 10.0

    # 4. Novelty / pattern interrupt
    novelty_hits = sum(1 for w in ("contrarian", "experiment", "behind", "teardown", "unpopular", "data", "case study") if w in combined)
    novelty_score = 50.0 + min(40.0, novelty_hits * 13.0)

    # 5. Shareability
    share_hits = sum(1 for t in SHARE_TRIGGERS if t in combined)
    share_score = 50.0 + min(38.0, share_hits * 12.0)

    # 6. Retention potential
    has_structure = len(req.concept.split()) >= 18
    retention_score = 54.0 + (20.0 if has_structure else 4.0) + (12.0 if any(w in combined for w in ("step", "part", "reveal", "result", "before")) else 0.0)

    # 7. Visual appeal
    visual_score = 76.0 if len(req.visual_plan.strip()) >= 12 else 48.0

    # 8. Timing
    timing_lower = req.timing_context.lower()
    timing_score = 78.0 if any(w in timing_lower for w in ("trending", "breaking", "seasonal", "launch", "2026")) else 62.0

    # 9. Trend relevance
    trend_score = 76.0 if any(w in combined for w in ("ai", "trend", "new", "2026", "shift", "algorithm")) else 58.0

    # 10. Competition (higher score = lower saturation / sharper angle)
    comp_score = 74.0 if aud_specific and novelty_hits > 0 else 54.0

    # 11. Platform compatibility
    plat = req.platform.lower()
    plat_score = 68.0
    if "reels" in plat or "shorts" in plat or "tiktok" in plat:
        plat_score = 84.0 if word_count <= 14 and len(req.visual_plan.strip()) > 0 else 64.0
    elif "linkedin" in plat or "x" in plat:
        plat_score = 82.0 if any(w in combined for w in ("framework", "data", "lesson", "case")) else 66.0

    raw_scores = {
        "hook_strength": (_clamp(hook_score), f"Hook length is {word_count} words with {'strong' if hook_score >= 70 else 'moderate'} curiosity/specificity cues."),
        "emotional_impact": (_clamp(emo_score), f"Detected {emo_hits} emotional/stakes triggers across hook and concept."),
        "audience_relevance": (_clamp(aud_score), "Specific audience targeting increases algorithmic matching." if aud_specific else "Audience is broad ('general'); narrow to a specific persona."),
        "novelty": (_clamp(novelty_score), "Evaluates pattern-interrupt framing and original angle."),
        "shareability": (_clamp(share_score), "Measures save/send-to-a-friend utility and social currency."),
        "retention_potential": (_clamp(retention_score), "Evaluates narrative payoff, pacing cues, and mid-video curiosity loops."),
        "visual_appeal": (_clamp(visual_score), "Visual direction specified." if visual_score >= 70 else "No concrete visual/B-roll direction provided."),
        "timing": (_clamp(timing_score), f"Timing context: {req.timing_context}."),
        "trend_relevance": (_clamp(trend_score), "Alignment with active cultural or category conversations."),
        "competition": (_clamp(comp_score), "Differentiation against saturated category angles."),
        "platform_compatibility": (_clamp(plat_score), f"Fit for {req.platform} format and consumption habits."),
    }

    dimensions: List[DimensionScore] = []
    weighted_sum = 0.0
    for key, weight in DIMENSION_WEIGHTS.items():
        sc, rat = raw_scores[key]
        weighted_sum += sc * weight
        dimensions.append(DimensionScore(dimension=key, score=sc, weight=weight, rationale=rat))

    calibration = learning_store.get_calibration_offset(req.platform)
    cal_offset = 0.0
    if calibration["sample_count"] >= 3:
        # Apply bounded calibration adjustment (+/- 10 pts max)
        cal_offset = max(-10.0, min(10.0, calibration["mean_bias"] * 0.5))

    final_score = _clamp(weighted_sum + cal_offset)
    sorted_dims = sorted(dimensions, key=lambda d: d.score, reverse=True)
    strengths = [f"{d.dimension.replace('_', ' ').title()} ({d.score}/100): {d.rationale}" for d in sorted_dims[:3]]
    weaknesses = [f"{d.dimension.replace('_', ' ').title()} ({d.score}/100): {d.rationale}" for d in sorted_dims[-3:]]

    improvements = []
    if raw_scores["hook_strength"][0] < 75:
        improvements.append("Compress the opening hook under 10 words and add a concrete number or contrarian tension.")
    if raw_scores["visual_appeal"][0] < 70:
        improvements.append("Add a first-3-second visual pattern interrupt (on-screen proof, split-screen, or physical prop).")
    if raw_scores["audience_relevance"][0] < 70:
        improvements.append("Call out the exact target persona in the first sentence so platform classifiers match faster.")
    if not req.cta.strip():
        improvements.append("Add a low-friction save/share CTA tied to a concrete takeaway.")
    if not improvements:
        improvements.append("A/B test two opening 3-second frames while keeping the body script constant.")

    alternatives = [
        {
            "angle": "Contrarian Teardown",
            "hook": f"Stop doing {req.niche} the old way — here is what actually moves the needle for {req.target_audience}",
            "why": "Creates an immediate pattern interrupt and curiosity gap.",
        },
        {
            "angle": "Data & Proof Experiment",
            "hook": f"We tested 3 approaches to {req.niche} — only 1 worked for {req.target_audience}",
            "why": "Signals empirical proof and high retention until the reveal.",
        },
        {
            "angle": "Saveable Checklist",
            "hook": f"The 3-step {req.niche} checklist every {req.target_audience} saves before starting",
            "why": "Optimizes for saves and shares, key non-follower distribution signals.",
        },
    ]

    conf = "High (Calibrated)" if calibration["sample_count"] >= 5 else ("Medium" if len(req.concept) > 40 else "Low (Sparse Input)")
    cal_note = (
        f"Calibrated with {calibration['sample_count']} logged {req.platform} campaigns (offset {cal_offset:+.1f} pts)."
        if calibration["sample_count"] > 0
        else "Uncalibrated baseline heuristic (0 logged campaigns for this platform yet). Log campaign outcomes to calibrate."
    )

    rec_platform = req.platform
    if raw_scores["visual_appeal"][0] < 55 and "reels" in plat:
        rec_platform = "linkedin or x (text-first) until visual direction is added"

    return ViralityScoreResponse(
        viral_potential_score=final_score,
        confidence_level=conf,
        calibration_note=cal_note,
        dimension_scores=dimensions,
        biggest_strengths=strengths,
        biggest_weaknesses=weaknesses,
        improvements_required=improvements,
        alternative_versions=alternatives,
        recommended_platform=rec_platform,
        methodology_disclaimer=(
            "Heuristic & empirically calibrated score (0-100). It estimates relative creative strength "
            "and is NOT a guarantee of virality or a fixed growth percentage."
        ),
    )
