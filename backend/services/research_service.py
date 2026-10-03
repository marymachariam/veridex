import json
import logging
from typing import Any, Dict, List, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph
from tavily import TavilyClient

from core.config import settings
from services.scraper_service import scrape_competitor_pages

logger = logging.getLogger("veridex.research")

MODEL_NAME = "openai/gpt-oss-120b"
GEMINI_MODEL_NAME = "gemini-3.8-flash"
MAX_TOOL_ROUNDS = 4

SYSTEM_PROMPT = """You are a professional competitive intelligence analyst. You research a real company \
using the web_search tool and any scraped website content provided to you, and produce a structured \
competitor analysis following this exact standardized framework, used consistently across every report \
so results are comparable company to company:

1. COMPANY OVERVIEW - what they do, founding year if findable, headquarters
2. TARGET MARKET - who they sell to
3. POSITIONING - their tagline/value proposition, how they differentiate
4. PRICING & PACKAGING - every publicly listed pricing tier with price and billing period. If pricing is \
hidden/"contact sales," say so - never invent a number. Prefer scraped website content over search results \
for pricing, since it is ground truth.
5. KEY FEATURES - the 5-10 features they most prominently market
6. SWOT - Strengths, Weaknesses, Opportunities, Threats, each grounded in what you actually found
7. RECENT SIGNALS - recent funding, hires, launches, or news (last 12 months if findable)
8. SOURCES - the URLs you actually used

Use web_search as many times as you need (up to a few searches) to cover pricing, positioning, and recent \
news specifically - a single generic search is not enough. Once you have enough information, respond with \
ONLY a single JSON object, no markdown fences, no commentary, matching exactly this shape:
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


@tool
def web_search(query: str) -> str:
    """Search the web for current information. Returns titles, URLs, and short excerpts."""
    client = TavilyClient(api_key=settings.TAVILY_API_KEY)
    results = client.search(query, max_results=5, search_depth="advanced")
    lines = []
    for r in results.get("results", []):
        lines.append(f"URL: {r.get('url')}\nTITLE: {r.get('title')}\nCONTENT: {r.get('content', '')[:800]}")
    return "\n\n".join(lines) if lines else "No results found."


class ResearchState(TypedDict):
    messages: List[Any]
    rounds: int


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
        # Output was truncated (often from a rate-limit retry cutting it short mid-array).
        last_complete = candidate.rfind("},")
        if last_complete != -1:
            repaired = candidate[:last_complete + 1] + "]}" if "[" in candidate[last_complete:] else candidate[:last_complete + 1] + "}"
            try:
                return json.loads(repaired)
            except json.JSONDecodeError:
                pass
        raise


def _candidate_llms():
    """Yields (label, llm) pairs to try in order: every Groq key first, then every Gemini key.
    One rate-limited or exhausted key never blocks a user - we just move to the next one."""
    for key in settings.groq_api_key_list:
        yield ("groq", ChatGroq(model=MODEL_NAME, api_key=key, temperature=0.1))

    if settings.gemini_api_key_list:
        from langchain_google_genai import ChatGoogleGenerativeAI
        for key in settings.gemini_api_key_list:
            yield ("gemini", ChatGoogleGenerativeAI(model=GEMINI_MODEL_NAME, api_key=key, temperature=0.1))


def _build_graph(llm):
    llm_with_tools = llm.bind_tools([web_search])

    def call_model(state: ResearchState) -> ResearchState:
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": state["messages"] + [response], "rounds": state["rounds"] + 1}

    def call_tools(state: ResearchState) -> ResearchState:
        last = state["messages"][-1]
        tool_messages = []
        for call in last.tool_calls:
            result = web_search.invoke(call["args"])
            tool_messages.append(ToolMessage(content=result, tool_call_id=call["id"]))
        return {"messages": state["messages"] + tool_messages, "rounds": state["rounds"]}

    def should_continue(state: ResearchState) -> str:
        last = state["messages"][-1]
        has_calls = isinstance(last, AIMessage) and getattr(last, "tool_calls", None)
        if has_calls and state["rounds"] < MAX_TOOL_ROUNDS:
            return "tools"
        return END

    graph = StateGraph(ResearchState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", call_tools)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")
    return graph.compile()


def research_competitor(name: str, website: str = None, category: str = None) -> Dict[str, Any]:
    if not settings.TAVILY_API_KEY:
        raise RuntimeError("TAVILY_API_KEY is not configured on the server")

    scraped_text = scrape_competitor_pages(website) if website else ""

    hints = f" Their website is {website}." if website else ""
    hints += f" They are known to be in the {category} category." if category else ""

    if scraped_text:
        user_prompt = (
            f"Research the company '{name}'.{hints} Follow the standardized framework exactly.\n\n"
            f"Here is real scraped content directly from their website - treat this as ground truth "
            f"and prefer it over anything found via search, especially for pricing:\n\n{scraped_text}"
        )
    else:
        user_prompt = f"Research the company '{name}'.{hints} Follow the standardized framework exactly."

    last_error = None
    tried_any = False

    for label, llm in _candidate_llms():
        tried_any = True
        try:
            app = _build_graph(llm)
            final_state = app.invoke({
                "messages": [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=user_prompt)],
                "rounds": 0,
            })
            last_message = final_state["messages"][-1]
            text = last_message.content if isinstance(last_message.content, str) else str(last_message.content)
            return _extract_json(text)
        except (ValueError, json.JSONDecodeError) as exc:
            logger.warning("Parse failed on %s: %s", label, exc)
            last_error = exc
            continue
        except Exception as exc:
            logger.warning("Provider %s failed (likely rate limit or auth): %s", label, exc)
            last_error = exc
            continue

    if not tried_any:
        raise RuntimeError("No GROQ_API_KEYS or GEMINI_API_KEYS configured on the server")

    logger.error("All providers failed for research on %s", name)
    raise RuntimeError("Could not complete research right now. Please try again shortly.") from last_error