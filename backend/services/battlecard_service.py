import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from core.config import settings

logger = logging.getLogger("veridex.battlecard")

SYSTEM_PROMPT = """You are a senior sales enablement writer. You are given structured research data about a \
competitor (pricing, features, SWOT). Produce a sales battlecard: a short, punchy, practical reference a \
salesperson can glance at during a live call when a prospect mentions this competitor.

Rules:
- Be concrete and specific, grounded only in the data given - never invent features, prices or claims not \
present in the input.
- "why_we_win" and "watch_out_for" should be short punchy phrases (under 15 words each), not paragraphs.
- "objection_handling" should anticipate 2-3 realistic things a prospect might say in favor of the \
competitor, each with a short suggested response.
- If the input data is sparse (e.g. no SWOT), work with what's there rather than refusing.

Respond with ONLY a single JSON object, no markdown fences, no commentary, matching exactly this shape:
{
  "one_liner": "<one sentence: who this competitor is and their angle>",
  "why_we_win": ["...", "..."],
  "watch_out_for": ["...", "..."],
  "objection_handling": [{"objection": "...", "response": "..."}],
  "pricing_summary": "<1-2 sentence plain-English summary of their pricing>"
}"""


def _extract_json(text: str) -> Dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in model output")
    candidate = text[start:end + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        from json_repair import repair_json
        return json.loads(repair_json(candidate))


def generate_battlecard(competitor_name: str, pricing: list, features: list, insight: dict) -> Dict[str, Any]:
    keys = settings.groq_api_key_list
    if not keys:
        raise RuntimeError("No GROQ_API_KEYS configured on the server")

    input_data = {
        "competitor_name": competitor_name,
        "pricing": pricing,
        "features": features,
        "insight": insight,
    }
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=json.dumps(input_data, indent=2)),
    ]

    last_error = None
    for key in keys:
        try:
            llm = ChatGroq(model="openai/gpt-oss-120b", api_key=key, temperature=0.2, max_retries=0, timeout=45)
            response = llm.invoke(messages)
            text = response.content if isinstance(response.content, str) else str(response.content)
            return _extract_json(text)
        except Exception as exc:
            logger.warning("Battlecard generation failed on one key: %s", exc)
            last_error = exc

    logger.error("All Groq keys failed for battlecard on %s", competitor_name)
    raise RuntimeError("Could not generate the battlecard. Try again.") from last_error