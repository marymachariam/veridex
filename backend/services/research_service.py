import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Any, Callable, Dict, List, Tuple

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from tavily import TavilyClient

from core.config import settings
from services.scraper_service import scrape_competitor_pages

logger = logging.getLogger("veridex.research")

MODEL_NAME = "openai/gpt-oss-120b"
GEMINI_MODEL_NAME = "gemini-2.0-flash"

MAX_SEARCH_RESULTS = 4
SNIPPET_CHARS = 500
MAX_CONTEXT_CHARS = 20000   
DEADLINE_SECONDS = 60

SYSTEM_PROMPT = """You are a professional competitive intelligence analyst. You are given scraped website \
content (labelled by page, with its source URL) and web search results about a real company, and you produce \
a structured competitor analysis following this exact standardized framework, used consistently across every \
report so results are comparable company to company:

1. COMPANY OVERVIEW - what they do, founding year if findable, headquarters
2. TARGET MARKET - who they sell to
3. POSITIONING - their tagline/value proposition, how they differentiate
4. PRICING & PACKAGING - every publicly listed pricing tier
5. KEY FEATURES - the 5-10 features they most prominently market
6. SWOT - Strengths, Weaknesses, Opportunities, Threats, each grounded in what you actually found
7. RECENT SIGNALS - recent funding, hires, launches, or news (last 12 months if findable)
8. SOURCES - the URLs you actually used

GROUNDING RULES (these matter most):
- Every fact must come from the scraped website content or the search results provided. If you could not \
find something, use null or an empty list. Never guess and never fill gaps from memory.
- The scraped content is labelled by page, with its source URL. Treat it as ground truth.

PRICING RULES:
- When a PRICING PAGE section is provided, take pricing ONLY from it. List EVERY tier in the order shown, \
including free tiers ($0) and tiers marked "contact sales" (use price_usd null for those).
- Use the exact tier names and the exact numbers shown. Do not convert, round or estimate.
- In each tier's "description", state what the price is per (for example "per member / month", "per seat", \
"flat rate"), and the audience or main limits the page gives for that tier.
- billing_period: use "monthly" or "annual" only if the page makes clear which one the displayed price is. \
If the page has a monthly/yearly toggle and does not say which price is shown, use "monthly" and add \
"billing period not stated on page" to the description.
- If there is no pricing page content and the search results do not show prices, return an empty pricing \
list. Never invent a number.

FEATURES RULES:
- Use the features/product pages and the feature lists inside the pricing tiers. For each feature, set \
tier_available to the lowest tier that includes it when the page shows that, otherwise null.

SOURCES RULES:
- "sources" must contain only URLs that were labelled in the scraped content or that appeared in the \
search results. Include the pricing page URL whenever pricing came from it.

Respond with ONLY a single JSON object, no markdown fences, no commentary, matching exactly this shape:
{
  "founded_year": <int or null>,
  "category": "<short category label>",
  "website": "<domain, no https://>",
  "tagline": "<their stated tagline/value prop, or null>",
  "target_market": "<1-2 sentences>",
  "summary": "<3-4 sentence overview>",
  "pricing": [{"tier_name": "...", "price_usd": <float or null>, "billing_period": "monthly|annual", "description": "..."}],
  "features": [{"feature_name": "...", "tier_available": "<tier name or null>"}],
  "strengths": ["...", "..."],
  "weaknesses": ["...", "..."],
  "opportunities": ["...", "..."],
  "threats": ["...", "..."],
  "recent_signals": ["...", "..."],
  "sources": ["https://...", "https://..."]
}"""


# ---------------------------------------------------------------------------
# Step 1: gather evidence (web search, in parallel)
# ---------------------------------------------------------------------------

def _tavily_search(client: TavilyClient, query: str) -> str:
    try:
        results = client.search(query, max_results=MAX_SEARCH_RESULTS, search_depth="basic")
    except Exception as exc:
        logger.warning("Search failed for %r: %s", query, exc)
        return f"SEARCH: {query}\n(no results)"

    lines = [
        f"URL: {r.get('url')}\nTITLE: {r.get('title')}\nCONTENT: {(r.get('content') or '')[:SNIPPET_CHARS]}"
        for r in results.get("results", [])
    ]
    return f"SEARCH: {query}\n" + ("\n\n".join(lines) if lines else "(no results)")


def _gather_search_context(name: str, has_pricing_page: bool) -> str:
    year = datetime.now().year
    queries = [
        f"{name} company overview target market positioning",
        f"{name} recent news funding launches {year}",
        f"{name} customer reviews pros and cons",
    ]
    if not has_pricing_page:
        queries.insert(0, f"{name} pricing plans")

    client = TavilyClient(api_key=settings.TAVILY_API_KEY)
    with ThreadPoolExecutor(max_workers=len(queries)) as pool:
        return "\n\n".join(pool.map(lambda q: _tavily_search(client, q), queries))


def _build_user_prompt(name: str, website: str, category: str, scraped_text: str, search_text: str) -> str:
    hints = f" Their website is {website}." if website else ""
    hints += f" They are known to be in the {category} category." if category else ""

    parts = [f"Research the company '{name}'.{hints} Follow the standardized framework and all rules exactly."]
    if scraped_text:
        parts.append("WEBSITE CONTENT (scraped directly from their site, treat as ground truth):\n" + scraped_text)
    parts.append("WEB SEARCH RESULTS:\n" + search_text)

    prompt = "\n\n".join(parts)
    if len(prompt) > MAX_CONTEXT_CHARS:
        prompt = prompt[:MAX_CONTEXT_CHARS] + "\n\n[content truncated]"
    return prompt


# ---------------------------------------------------------------------------
# Step 2: one AI call
# ---------------------------------------------------------------------------

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
        pass

    # Try truncating at the last complete entry (common when output gets cut off mid-array).
    last_complete = candidate.rfind("},")
    if last_complete != -1:
        repaired = candidate[:last_complete + 1] + "]}" if "[" in candidate[last_complete:] else candidate[:last_complete + 1] + "}"
        try:
            return json.loads(repaired)
        except json.JSONDecodeError:
            pass

    # Last resort: use json_repair for subtler syntax issues (unescaped quotes, stray commas, etc.)
    from json_repair import repair_json
    return json.loads(repair_json(candidate))


def _llm_builders() -> List[Tuple[str, Callable[[], Any]]]:
    """(label, builder) pairs tried in order: every Groq key first, then every Gemini key.
    Builders are called inside the try block, so a bad setting can never crash the whole request."""
    builders: List[Tuple[str, Callable[[], Any]]] = []

    for key in settings.groq_api_key_list:
        builders.append((
            "groq",
            lambda key=key: ChatGroq(
                model=MODEL_NAME, api_key=key, temperature=0.1, max_tokens=2500, max_retries=0, timeout=45
            ),
        ))

    for key in settings.gemini_api_key_list:
        def build_gemini(key=key):
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model=GEMINI_MODEL_NAME, api_key=key, temperature=0.1, max_retries=1, timeout=45
            )
        builders.append(("gemini", build_gemini))

    return builders


def research_competitor(name: str, website: str = None, category: str = None) -> Dict[str, Any]:
    if not settings.TAVILY_API_KEY:
        raise RuntimeError("TAVILY_API_KEY is not configured on the server")

    builders = _llm_builders()
    if not builders:
        raise RuntimeError("No GROQ_API_KEYS or GEMINI_API_KEYS configured on the server")

    scraped_text = scrape_competitor_pages(website) if website else ""
    search_text = _gather_search_context(name, "PRICING PAGE" in scraped_text)
    user_prompt = _build_user_prompt(name, website, category, scraped_text, search_text)
    logger.info("Research prompt for %s: %d characters", name, len(user_prompt))

    messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=user_prompt)]

    started = time.monotonic()
    last_error = None

    for label, build in builders:
        if time.monotonic() - started > DEADLINE_SECONDS:
            logger.warning("Research deadline reached, not trying more providers")
            break
        try:
            response = build().invoke(messages)
            text = response.content if isinstance(response.content, str) else str(response.content)
            return _extract_json(text)
        except (ValueError, json.JSONDecodeError) as exc:
            logger.warning("Parse failed on %s: %s", label, exc)
            last_error = exc
        except Exception as exc:
            logger.warning("Provider %s failed (likely rate limit or auth): %s", label, exc)
            last_error = exc

    logger.error("All providers failed for research on %s", name)
    message = str(last_error).lower() if last_error else ""
    if any(t in message for t in ("429", "rate limit", "quota", "resource_exhausted", "413", "too large")):
        raise RuntimeError(
            "Our AI provider is busy (free-tier limit reached). Please wait a minute and try again."
        ) from last_error
    raise RuntimeError("Could not complete research right now. Please try again shortly.") from last_error