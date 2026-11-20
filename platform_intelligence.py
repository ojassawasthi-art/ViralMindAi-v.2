"""Platform Algorithm & Viral Pattern Intelligence Engine.

Strictly separates verified official platform documentation from observed patterns and hypotheses.
Never invents secret algorithm hacks.
"""

from __future__ import annotations

from typing import Any, Dict, List


PLATFORM_KNOWLEDGE: Dict[str, Dict[str, Any]] = {
    "youtube": {
        "display_name": "YouTube (Long-Form & Shorts)",
        "verified_official_signals": [
            "Viewer satisfaction surveys, watch time, and clicks/impressions (CTR) guide recommendations.",
            "YouTube evaluates each video against viewer history rather than a single global score; Shorts and Long-form have distinct discovery surfaces.",
            "Focus on audience fit ('Does my audience like this?') rather than chasing 'the algorithm'.",
        ],
        "official_sources": [
            {
                "title": "On YouTube's recommendation system",
                "url": "https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/",
            },
            {
                "title": "YouTube's Recommendation System - Google Help",
                "url": "https://support.google.com/youtube/answer/16533387?hl=en",
            },
            {
                "title": "How YouTube recommendations work",
                "url": "https://support.google.com/youtube/answer/16089387?hl=en",
            },
        ],
        "observed_patterns": [
            "Thumbnails + titles that create a clear curiosity gap without clickbait mismatch sustain higher 30-second retention.",
            "Shorts with >70% viewed-vs-swiped-away rate and strong loop/rewatch endings expand into broader test cohorts.",
        ],
        "testable_hypotheses": [
            "Testing 2 thumbnail concepts via YouTube's native Test & Compare can lift CTR without altering video content.",
            "Structuring long-form intros with an immediate visual proof clip in the first 15 seconds reduces early drop-off.",
        ],
    },
    "instagram": {
        "display_name": "Instagram (Reels, Feed, Carousels, Stories)",
        "verified_official_signals": [
            "Instagram uses separate ranking systems for Feed, Stories, Reels, Explore, and Search.",
            "For Reels and Feed, key signals include user past activity, post popularity/interaction speed, and relationship/interaction history with the creator.",
            "Originality is prioritized over reposted/watermarked aggregator content.",
        ],
        "official_sources": [
            {
                "title": "Instagram Ranking Explained (Adam Mosseri)",
                "url": "https://about.instagram.com/blog/announcements/instagram-ranking-explained",
            },
            {
                "title": "Shedding More Light on How Instagram Works",
                "url": "https://about.instagram.com/blog/announcements/shedding-more-light-on-how-instagram-works",
            },
        ],
        "observed_patterns": [
            "DM sends/shares per reach and saves per reach strongly correlate with non-follower Reels distribution.",
            "Educational carousels with a bold slide-1 promise and swipeable micro-steps drive high save rates.",
        ],
        "testable_hypotheses": [
            "Adding a 1-sentence 'send this to someone who...' prompt mid-Reel increases shares-per-reach.",
            "Using native text overlays readable in safe zones improves 3-second hold rate.",
        ],
    },
    "tiktok": {
        "display_name": "TikTok (For You Feed)",
        "verified_official_signals": [
            "For You feed ranks videos based on user interactions (likes, shares, comments, follows, watch completion), video information (captions, sounds, hashtags), and device/account settings.",
            "Follower count is not a direct ranking factor for For You recommendations.",
        ],
        "official_sources": [
            {
                "title": "How TikTok recommends videos #ForYou",
                "url": "https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you",
            },
            {
                "title": "How TikTok recommends content - Support",
                "url": "https://support.tiktok.com/en/using-tiktok/exploring-videos/how-tiktok-recommends-content",
            },
        ],
        "observed_patterns": [
            "Search-intent keywords in spoken audio, on-screen text, and captions improve TikTok Search discovery.",
            "Pattern-interrupt visual cuts every 2-4 seconds sustain completion rates on 20-45s explainers.",
        ],
        "testable_hypotheses": [
            "Answering a specific niche search query in the first 3 seconds captures both For You and Search traffic.",
        ],
    },
    "linkedin": {
        "display_name": "LinkedIn",
        "verified_official_signals": [
            "Prioritizes relevant knowledge sharing, professional conversations, and meaningful comments within topic networks.",
        ],
        "official_sources": [
            {
                "title": "LinkedIn Engineering & Feed Relevance",
                "url": "https://www.linkedin.com/help/linkedin/answer/a1340595",
            }
        ],
        "observed_patterns": [
            "Document/PDF carousels, first-hand case studies with real numbers, and native frameworks outperform outbound link posts.",
        ],
        "testable_hypotheses": [
            "Replacing external links in the post body with a native summary + link in comments preserves initial dwell time.",
        ],
    },
    "x": {
        "display_name": "X (Twitter)",
        "verified_official_signals": [
            "Ranks posts based on engagement velocity (replies, reposts, bookmarks, likes), media richness, and network graph relevance.",
        ],
        "official_sources": [
            {
                "title": "X Open-Source Recommendation Algorithm",
                "url": "https://github.com/twitter/the-algorithm",
            }
        ],
        "observed_patterns": [
            "Bookmark-worthy threads, visual diagrams, and sharp contrarian observations earn longer dwell time and reposts.",
        ],
        "testable_hypotheses": [
            "Posting a standalone 1-image summary chart outperforms text-only threads for cold-audience discovery.",
        ],
    },
}

ADDITIONAL_PLATFORMS = ["facebook_reels", "pinterest", "reddit", "threads", "snapchat"]


def analyze_platform(platform: str) -> Dict[str, Any]:
    key = platform.lower().strip()
    if "youtube" in key:
        key = "youtube"
    elif "instagram" in key or "reels" in key:
        key = "instagram"
    elif "tiktok" in key:
        key = "tiktok"
    elif "linkedin" in key:
        key = "linkedin"
    elif key in ("x", "twitter"):
        key = "x"

    if key in PLATFORM_KNOWLEDGE:
        data = PLATFORM_KNOWLEDGE[key]
        return {
            "platform": key,
            "epistemic_note": "Strictly separates verified official documentation from observed patterns and testable hypotheses.",
            **data,
        }

    return {
        "platform": key,
        "display_name": key.replace("_", " ").title(),
        "epistemic_note": "General cross-platform principles; verify platform-specific creator documentation before scaling.",
        "verified_official_signals": [
            "Platforms optimize for user satisfaction, watch/dwell completion, and authentic interactions (shares, saves, replies) while downranking spam or unoriginal reposts."
        ],
        "official_sources": [],
        "observed_patterns": [
            "Native vertical video (9:16) or native high-contrast carousels with clear 3-second hooks outperform cross-posted watermarked links."
        ],
        "testable_hypotheses": [
            "Adapt aspect ratio, caption length, and community tone natively for this platform before judging performance."
        ],
        "supported_deep_profiles": list(PLATFORM_KNOWLEDGE.keys()) + ADDITIONAL_PLATFORMS,
    }


def list_supported_platforms() -> List[str]:
    return list(PLATFORM_KNOWLEDGE.keys()) + ADDITIONAL_PLATFORMS
