import requests
import streamlit as st

from config import settings

STEPS = [
    {
        "icon": "",
        "title": "Welcome to Veridex",
        "body": "Veridex researches your competitors for you: their pricing, features, positioning and "
                "customer sentiment. This quick tour takes about a minute. You're on a **14-day free trial**, "
                "so everything is open for you to explore.",
    },
    {
        "icon": "",
        "title": "Your Dashboard",
        "body": "This is your home base. It shows the number of competitors you track, their pricing tiers, "
                "reviews and quick buttons to jump anywhere in the app.",
    },
    {
        "icon": "",
        "title": "Research a competitor",
        "body": "Open **Research**, type a company name (a website is optional) and click **Run Research**. "
                "In about 20-40 seconds you get an overview, pricing, key features, a SWOT analysis and "
                "recent news about them.",
    },
    {
        "icon": "",
        "title": "Research History",
        "body": "Every research you run is saved exactly as it was returned. Open **History** any time to "
                "search past runs and read them again, without running the research a second time.",
    },
    {
        "icon": "",
        "title": "Your Competitors",
        "body": "**Competitors** lists every company you track. You can add one manually, select two or more "
                "to compare, or open a **Battlecard**, a quick summary sheet for one competitor.",
    },
    {
        "icon": "⚖️",
        "title": "Compare side by side",
        "body": "Pick competitors and use **Compare** to see them next to each other, so you can spot gaps "
                "and opportunities quickly.",
    },
    {
        "icon": "",
        "title": "Pricing, History & Sentiment",
        "body": "**Pricing Analysis** and **Price History** show what competitors charge and how it changes "
                "over time. **Sentiment Analysis** shows what customers like and dislike about them.",
    },
    {
        "icon": "",
        "title": "Alerts",
        "body": "**Alerts** tells you when something changes at a competitor, like new pricing, new features "
                "or a shift in positioning, so you never miss a move.",
    },
    {
        "icon": "",
        "title": "Plans & Billing",
        "body": "Your trial lasts 14 days. When you're ready, the **Billing** page lets you pick a plan and "
                "pay with PayPal.",
    },
    {
        "icon": "",
        "title": "Need help? Ask Veridex AI",
        "body": "See the glowing **Ask Veridex AI** button in the bottom-right corner of every page? Ask it "
                "anything about using Veridex, any time.",
    },
    {
        "icon": "",
        "title": "You're all set!",
        "body": "That's everything you need to get started. The best way to learn is to try it: "
                "research your first competitor now.",
    },
]


def _headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}


def _needs_onboarding() -> bool:
    try:
        r = requests.get(
            f"{settings.API_BASE_URL}/api/v1/auth/me", headers=_headers(), timeout=settings.API_TIMEOUT
        )
        return r.status_code == 200 and r.json().get("onboarding_completed") is False
    except requests.RequestException:
        return False


def _mark_complete():
    try:
        requests.post(
            f"{settings.API_BASE_URL}/api/v1/auth/onboarding/complete",
            headers=_headers(),
            timeout=settings.API_TIMEOUT,
        )
    except requests.RequestException:
        pass 


def _next():
    st.session_state.tour_step += 1


def _back():
    st.session_state.tour_step -= 1


@st.dialog("Veridex Tour", width="large")
def _tour_dialog():
    step = st.session_state.get("tour_step", 0)
    total = len(STEPS)
    s = STEPS[step]
    last = step == total - 1

    st.progress((step + 1) / total, text=f"Step {step + 1} of {total}")
    st.markdown(f"<div style='text-align:center; font-size:60px; margin-top:0.5rem;'>{s['icon']}</div>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center; margin-bottom:0.5rem;'>{s['title']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:16px; line-height:1.6;'>{s['body']}</p>", unsafe_allow_html=True)
    st.write("")

    if last:
        if st.button(" Start my first research", type="primary", width="stretch"):
            _mark_complete()
            st.session_state.tour_needed = False
            st.session_state.tour_goto = "pages/09_Research.py"
            st.rerun()
        if st.button("Finish tour", width="stretch"):
            _mark_complete()
            st.session_state.tour_needed = False
            st.rerun()
    else:
        c_skip, c_back, c_next = st.columns([1.3, 1, 1.3])
        with c_skip:
            if st.button("Skip tour", width="stretch"):
                _mark_complete()
                st.session_state.tour_needed = False
                st.rerun()
        with c_back:
            st.button("← Back", on_click=_back, disabled=(step == 0), width="stretch")
        with c_next:
            st.button("Next →", on_click=_next, type="primary", width="stretch")


def maybe_show_tour():
    """Call once near the top of the Dashboard. Opens the tour for brand-new accounts only."""
    goto = st.session_state.pop("tour_goto", None)
    if goto:
        st.switch_page(goto)

    if "token" not in st.session_state:
        return

    if "tour_checked" not in st.session_state:
        st.session_state.tour_checked = True
        st.session_state.tour_needed = _needs_onboarding()

    if st.session_state.get("tour_needed") and not st.session_state.get("tour_opened"):
        st.session_state.tour_opened = True
        st.session_state.tour_step = 0
        _tour_dialog()


def replay_tour_button():
    """Optional: a small button so users can retake the tour any time."""
    if st.button(" Take the tour", width="stretch"):
        st.session_state.tour_step = 0
        _tour_dialog()