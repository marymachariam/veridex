import requests
import streamlit as st

from config import settings

SUGGESTIONS = [
    "How do I research a competitor?",
    "How does the 14-day trial work?",
    "What's included in the Pro plan?",
]

BOT_AVATAR = "assistant"

_CSS = """
<style>
/* Floating launcher */
.st-key-vx_bot {
    position: fixed !important;
    bottom: 24px;
    right: 24px;
    z-index: 999999;
    width: auto !important;
}
.st-key-vx_bot [data-testid="stPopoverButton"] {
    border-radius: 999px !important;
    background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
    border: none !important;
    padding: 0.7rem 1.3rem !important;
    box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.55) !important;
    animation: vx-pulse 2.8s ease-in-out infinite;
    transition: transform 0.2s ease;
}
.st-key-vx_bot [data-testid="stPopoverButton"]:hover { transform: translateY(-2px) scale(1.04); }
.st-key-vx_bot [data-testid="stPopoverButton"] p,
.st-key-vx_bot [data-testid="stPopoverButton"] span { color: #FFFFFF !important; font-weight: 600 !important; margin: 0; }
.st-key-vx_bot [data-testid="stPopoverButton"] svg { display: none; }
@keyframes vx-pulse {
    0%, 100% { box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.55); }
    50%      { box-shadow: 0 10px 38px 4px rgba(124, 58, 237, 0.7); }
}

/* Chat panel */
div[data-testid="stPopoverBody"] {
    width: 400px !important;
    max-width: 92vw !important;
    border-radius: 18px !important;
    padding: 0 !important;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.35) !important;
}
.vx-header {
    background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
    color: #FFFFFF;
    padding: 1rem 1.25rem;
    margin-bottom: 0.5rem;
}
.vx-header .t { font-size: 17px; font-weight: 700; }
.vx-header .s { font-size: 12.5px; opacity: 0.9; margin-top: 2px; }
.vx-dot { display:inline-block; width:8px; height:8px; border-radius:50%; background:#4ADE80; margin-right:6px; }

/* Suggestion chips */
[class*="st-key-vx_chip"] button {
    border-radius: 999px !important;
    font-size: 13px !important;
    padding: 0.25rem 0.8rem !important;
    border: 1px solid #C7D2FE !important;
}
[class*="st-key-vx_chip"] button:hover { border-color: #7C3AED !important; color: #7C3AED !important; }

/* Keep page-level "card" styling from leaking into the chat panel */
div[data-testid="stPopoverBody"] div[data-testid="stVerticalBlockBorderWrapper"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    border-radius: 0 !important;
}
/* Force a readable light look inside the chat panel on every page */
div[data-testid="stPopoverBody"] {
    background: #FFFFFF !important;
}
div[data-testid="stPopoverBody"] p,
div[data-testid="stPopoverBody"] li,
div[data-testid="stPopoverBody"] label,
div[data-testid="stPopoverBody"] [data-testid="stChatMessageContent"] {
    color: #0F172A !important;
}
div[data-testid="stPopoverBody"] button[kind="primary"] p {
    color: #FFFFFF !important;
}
div[data-testid="stPopoverBody"] input {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    background: #FFFFFF !important;
}
div[data-testid="stPopoverBody"] div[data-baseweb="input"] {
    background: #F8FAFC !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
}

/* Suggestion chips */
[class*="st-key-vx_chip"] button {
    background: #FFFFFF !important;
}
[class*="st-key-vx_chip"] button p {
    color: #4338CA !important;
    font-weight: 500 !important;
}
[class*="st-key-vx_chip"] button:hover p {
    color: #7C3AED !important;
}
</style>
"""

WELCOME = (
    "Hi! I'm **Veridex AI**. I can help you with researching competitors, "
    "your trial, plans, billing and anything else about Veridex. What would you like to know?"
)


def _ask(message: str, history: list) -> str:
    try:
        r = requests.post(
            f"{settings.API_BASE_URL}/api/v1/assistant/chat",
            json={"message": message, "history": history[-8:]},
            timeout=45,
        )
    except requests.RequestException:
        return "I can't reach the server right now. Please try again in a moment."

    if r.status_code == 200:
        return r.json().get("reply", "Sorry, something went wrong.")
    if r.status_code == 429:
        return "You're sending messages quickly. Give me a moment and try again. ⏳"
    return "Sorry, I couldn't answer that right now. Please try again."


def render_chatbot():
    st.markdown(_CSS, unsafe_allow_html=True)

    if "vx_bot_msgs" not in st.session_state:
        st.session_state.vx_bot_msgs = []
    history = st.session_state.vx_bot_msgs

    pending = st.session_state.pop("vx_bot_pending", None)

    with st.container(key="vx_bot"):
        with st.popover(" Ask Veridex AI"):
            st.markdown(
                '<div class="vx-header"><div class="t">✨ Veridex AI</div>'
                '<div class="s"><span class="vx-dot"></span>Ask me anything about Veridex</div></div>',
                unsafe_allow_html=True,
            )

            messages_box = st.container(height=330, border=False)
            chips_box = st.container()

            with st.form("vx_bot_form", clear_on_submit=True):
                c1, c2 = st.columns([5, 1])
                typed = c1.text_input(
                    "Message", placeholder="Ask about Veridex…", label_visibility="collapsed"
                )
                sent = c2.form_submit_button("➤", type="primary")

            question = pending or (typed.strip() if sent and typed else None)

            with messages_box:
                if not history and not question:
                    with st.chat_message(BOT_AVATAR):
                        st.markdown(WELCOME)
                for m in history:
                    with st.chat_message(m["role"]):
                        st.markdown(m["content"])
                if question:
                    with st.chat_message("user"):
                        st.markdown(question)
                    with st.chat_message(BOT_AVATAR):
                        with st.spinner("Thinking..."):
                            reply = _ask(question, history)
                        st.markdown(reply)
                    history.append({"role": "user", "content": question})
                    history.append({"role": "assistant", "content": reply})

            with chips_box:
                if not history:
                    for i, text in enumerate(SUGGESTIONS):
                        if st.button(text, key=f"vx_chip_{i}"):
                            st.session_state["vx_bot_pending"] = text
                            st.rerun()
                else:
                    if st.button("🗑 Clear chat", key="vx_chip_clear"):
                        st.session_state.vx_bot_msgs = []
                        st.rerun()