import requests
import streamlit as st

from config import settings, Icons
from utils.theme import apply_theme
from components.chatbot import render_chatbot

st.set_page_config(page_title=f"{settings.APP_NAME} - Alerts", layout="wide")
apply_theme()
render_chatbot()

if "token" not in st.session_state:
    st.switch_page("pages/01_Login.py")

st.markdown(f"# Competitor Alerts")
st.caption("Changes detected the last time each competitor was re-researched.")

headers = {"Authorization": f"Bearer {st.session_state.token}"}

try:
    comp_resp = requests.get(f"{settings.API_BASE_URL}/api/v1/competitors", headers=headers, params={"limit": 500}, timeout=settings.API_TIMEOUT)
    competitors = comp_resp.json() if comp_resp.status_code == 200 else []
except requests.RequestException:
    competitors = []

name_by_id = {c["id"]: c["name"] for c in competitors}

col1, col2 = st.columns([3, 1])
with col1:
    unread_only = st.checkbox("Show unread only", value=True)
with col2:
    if st.button("Mark all as read", width='stretch'):
        try:
            requests.post(f"{settings.API_BASE_URL}/api/v1/alerts/mark-all-read", headers=headers, timeout=settings.API_TIMEOUT)
            st.rerun()
        except requests.RequestException:
            st.error("Could not reach the server.")

try:
    resp = requests.get(
        f"{settings.API_BASE_URL}/api/v1/alerts",
        headers=headers,
        params={"unread_only": unread_only, "limit": 200},
        timeout=settings.API_TIMEOUT,
    )
    alerts = resp.json() if resp.status_code == 200 else []
except requests.RequestException:
    alerts = []

if not alerts:
    st.info("No alerts yet. Re-run Research on a competitor you've already tracked to check for changes.")
else:
    icon_by_type = {
        "pricing": "💰",
        "feature_added": "✨",
        "feature_removed": "🗑️",
        "positioning": "🎯",
    }
    for alert in alerts:
        comp_name = name_by_id.get(alert["competitor_id"], f"Competitor #{alert['competitor_id']}")
        icon = icon_by_type.get(alert["change_type"], "🔔")
        with st.container(border=True):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"{icon} **{comp_name}** — {alert['summary']}")
                st.caption(alert["detected_at"])
            with c2:
                if alert["is_read"] == 0:
                    if st.button("Mark read", key=f"read_{alert['id']}", width='stretch'):
                        try:
                            requests.post(
                                f"{settings.API_BASE_URL}/api/v1/alerts/{alert['id']}/mark-read",
                                headers=headers, timeout=settings.API_TIMEOUT,
                            )
                            st.rerun()
                        except requests.RequestException:
                            st.error("Could not reach the server.")
                else:
                    st.caption("✓ Read")