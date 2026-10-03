import logging
import time
from collections import defaultdict, deque
from typing import List, Literal

from fastapi import APIRouter, HTTPException, Request
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from core.config import settings
from services.assistant_knowledge import ASSISTANT_SYSTEM_PROMPT

logger = logging.getLogger("veridex.assistant")
router = APIRouter(prefix="/api/v1/assistant", tags=["assistant"])

# Simple in-memory rate limit: 20 messages per 5 minutes per client IP.
_WINDOW_SECONDS = 300
_MAX_MESSAGES = 20
_hits: dict = defaultdict(deque)


def _check_rate_limit(key: str) -> None:
    now = time.monotonic()
    q = _hits[key]
    while q and now - q[0] > _WINDOW_SECONDS:
        q.popleft()
    if len(q) >= _MAX_MESSAGES:
        raise HTTPException(status_code=429, detail="Too many messages. Please wait a moment.")
    q.append(now)


class ChatTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(max_length=2000)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    history: List[ChatTurn] = Field(default_factory=list, max_length=12)


class ChatResponse(BaseModel):
    reply: str


def _get_llm() -> ChatGroq:
    return ChatGroq(
        model=settings.GROQ_BOT_MODEL,
        api_key=settings.GROQ_BOT_API_KEY,
        temperature=0.2,
        max_tokens=800,
    )


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, request: Request):
    if not settings.GROQ_BOT_API_KEY:
        raise HTTPException(status_code=503, detail="Assistant is not configured")

    client_ip = request.client.host if request.client else "unknown"
    _check_rate_limit(client_ip)

    messages = [SystemMessage(content=ASSISTANT_SYSTEM_PROMPT)]
    for turn in payload.history[-8:]:
        messages.append(HumanMessage(content=turn.content) if turn.role == "user" else AIMessage(content=turn.content))
    messages.append(HumanMessage(content=payload.message))

    try:
        response = _get_llm().invoke(messages)
    except Exception:
        logger.exception("Assistant call failed")
        raise HTTPException(status_code=502, detail="The assistant is unavailable right now.")

    text = response.content if isinstance(response.content, str) else str(response.content)
    return ChatResponse(reply=text.strip() or "Sorry, I couldn't come up with an answer. Please try rephrasing.")