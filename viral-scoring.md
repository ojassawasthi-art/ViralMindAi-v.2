# Viral Potential Scoring Methodology (0–100)

The **Viral Potential Score** is a transparent, weighted creative evaluation — **not** a guarantee of virality.

## 11 Evaluated Dimensions
1. `hook_strength` (16%): Word count discipline, curiosity triggers, specificity/numbers.
2. `audience_relevance` (12%): Persona specificity and niche alignment.
3. `shareability` (12%): Save/send-to-a-friend utility and social currency.
4. `retention_potential` (12%): Narrative payoff, structure, and pacing cues.
5. `emotional_impact` (11%): Emotional stakes and resonance.
6. `novelty` (9%): Pattern-interrupt framing and contrarian/proof angles.
7. `visual_appeal` (8%): Presence of concrete first-3-second visual direction.
8. `timing` (5%): Evergreen vs. seasonal/breaking relevance.
9. `trend_relevance` (5%): Alignment with active cultural conversations.
10. `competition` (5%): Differentiation against saturated angles.
11. `platform_compatibility` (5%): Format and consumption fit.

## Empirical Calibration
When 3+ campaign outcomes are logged for a platform via `/api/v1/analytics/outcomes`, the engine computes `mean_bias = avg(actual_normalized_score - predicted_score)` and applies a bounded calibration offset (`+/- 10` pts max).
