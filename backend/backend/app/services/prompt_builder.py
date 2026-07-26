from __future__ import annotations

from typing import Any

DEFAULT_SESSION_TITLE_MAX_LENGTH = 80
DEFAULT_TOPIC_NAME = "General Python Learning"
PROMPT_PERSONA = (
    "You are NOVA, an AI learning assistant on AlgoLingo. "
    "Help students learn programming using space exploration metaphors. "
    "Call the user Captain or Explorer. Be concise, supportive, and practical. "
    "Keep most answers under 150 words unless debugging requires slightly more detail. "
    "Never reveal direct quiz answers. For practice help, guide instead of giving the full final solution unless the user explicitly requests debugging help. "
    "Format code using ```python blocks when useful."
)
MODE_HINT_INSTRUCTION = (
    "Mode: Hint generation. Provide 2-4 progressively helpful hints. "
    "Do not give the complete final answer or full solution code."
)
MODE_DEBUG_INSTRUCTION = (
    "Mode: Debugging. Identify the likely issue, explain why it happens, and provide a corrected example if needed."
)
MODE_RECOMMEND_INSTRUCTION = (
    "Mode: Recommendation. Suggest the next best learning step based on progress and quiz performance."
)
MODE_GENERAL_INSTRUCTION = "Mode: General concept explanation and learning support."
MODE_TO_PREFIX = {
    "hint": "Give me a hint for this practice challenge. ",
    "debug": "Help me debug this code. ",
    "recommend": "Recommend the next topic or review step for me. ",
}


class PromptBuilder:
    """Builds NOVA system and user prompts from runtime context."""

    @staticmethod
    def build_session_title(message: str, *, max_length: int = DEFAULT_SESSION_TITLE_MAX_LENGTH) -> str:
        """Builds a stable NOVA session title from the initial user message."""
        clean = " ".join(message.strip().split())
        if len(clean) <= max_length:
            return clean
        return clean[: max_length - 3].rstrip() + "..."

    @staticmethod
    def build_system_prompt(*, mode: str, context: dict[str, Any]) -> str:
        """Builds the NOVA system prompt for the requested interaction mode."""
        galaxy_name = (context.get("current_galaxy") or {}).get("name", "Unknown")
        planet_name = (context.get("current_planet") or {}).get("name", "Unknown")
        topic_name = context.get("current_topic") or DEFAULT_TOPIC_NAME
        level = context.get("user_level", 1)
        rank = context.get("user_rank", "Cadet")
        xp = context.get("user_xp", 0)
        streak = context.get("streak_days", 0)

        base_prompt = (
            f"{PROMPT_PERSONA}\n\n"
            f"Current Context:\n"
            f"- Galaxy: {galaxy_name}\n"
            f"- Planet: {planet_name}\n"
            f"- Topic: {topic_name}\n"
            f"- User Level: {level}\n"
            f"- User Rank: {rank}\n"
            f"- User XP: {xp}\n"
            f"- Current Streak: {streak} day(s)\n"
        )

        if mode == "hint":
            return base_prompt + MODE_HINT_INSTRUCTION
        if mode == "debug":
            return base_prompt + MODE_DEBUG_INSTRUCTION
        if mode == "recommend":
            return base_prompt + MODE_RECOMMEND_INSTRUCTION
        return base_prompt + MODE_GENERAL_INSTRUCTION

    @staticmethod
    def build_user_message(*, mode: str, raw_message: str, context: dict[str, Any]) -> str:
        """Builds the mode-specific user prompt with contextual supplements."""
        progress = context.get("user_progress") or {}
        recent_quiz_performance = context.get("recent_quiz_performance") or []
        recent_activity = context.get("recent_activity") or []

        supplemental = (
            f"\n\nUser progress summary: {progress}."
            f"\nRecent quiz performance: {recent_quiz_performance}."
            f"\nRecent activity: {recent_activity}."
        )

        return MODE_TO_PREFIX.get(mode, "") + raw_message + supplemental
